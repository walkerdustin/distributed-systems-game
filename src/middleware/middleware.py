"""
Here are all the sockets.
There shall not be any sockets outside of this file.

There shall be one socket in one seperate thread (multithreading)
for every tcp connections
also one socket in a thread for the udp socket for broadcast
"""

import threading
import socket
import ipaddress
from time import sleep
usleep = lambda x: sleep(x/1000_000.0) # sleep for x microseconds

from lib.myQueue import Q

######################################### PARAMETER Constants
BROADCAST_PORT = 61424
BUFFER_SIZE = 1024
SUBNETMASK = "255.255.255.0"
BROADCAST_LISTENER_SLEEP = 10 # microseconds

IP_ADRESS_OF_THIS_PC = socket.gethostbyname(socket.gethostname())
net = ipaddress.IPv4Network(IP_ADRESS_OF_THIS_PC + '/' + SUBNETMASK, False)
BROADCAST_IP = net.broadcast_address.exploded


class Middleware():
    deliveryQueue = Q()
    _holdBackQueue = Q()
    ipAdresses = {} # {uuid: (ipadress, port)} (str , int)

    def __init__(self,UUID):
        self.UUID = UUID     
        self._broadcastHandler = BroadcastHandler(UUID)
        self._unicastHandler = UnicastHandler()
        self._unicastHandler.subscribeUnicastListener(self._updateAdresses)

    @classmethod
    def addIpAdress(cls, uuid, addr):
        cls.ipAdresses[uuid] = addr

    def broadcastToAll(self, message):
        self._broadcastHandler.broadcast(message)
    
    def sendMessageTo(self, uuid, message): # unicast
        ipAdress = self.ipAdresses[uuid]
        self._unicastHandler.sendMessage(ipAdress, message)
    
    def sendIPAdressesto(self,uuid):
        s='updateIpAdresses:'
        for uuid, (addr,port) in self.ipAdresses.items():
            s += uuid+','+str(addr)+','+str(port)+'#'
        self.sendMessageTo(uuid,s)

    def subscribeBroadcastListener(self, observer_func):
        self._broadcastHandler.subscribeBroadcastListener(observer_func)
    
    def subscribeUnicastListener(self, observer_func):
        self._unicastHandler.subscribeUnicastListener(observer_func)
    def _updateAdresses(self, command:str, message:str):
         if command == 'updateIpAdresses':
            for addr in message.split('#'):
                addr = addr.split(',')
                self.addIpAdress(addr[0], (addr[1], int(addr[2])))


class UnicastHandler():

    def __init__(self):
        # Create a UDP socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._server_socket.bind(('', 0)) # ('', 0) '' use the lokal IP adress and 0 select a random open port
        self._serverPort = self._server_socket.getsockname()[1] # returns the previously selected (random) port

        self.incommingUnicastHistory = []
        self._listenerList = []

        # Create Thread to listen to UDP Broadcast
        self._listen_UDP_Unicast_Thread = threading.Thread(target=self._listenUnicast)
        self._listen_UDP_Unicast_Thread.start()

    
    def sendMessage(self, addr, message:str):
        self._server_socket.sendto(str.encode(message), addr)
        print('UnicastHandler: sent message: ', message,"\nto: ", addr)

    def _listenUnicast(self):
        print("listenUDP Unicast Thread has started and not blocked Progress (by running in the background)")
        while True:
            print('\nUnicastHandler: Waiting to receive unicast message...\n')
            # Receive message from client
            # Code waits here until it recieves a unicast to its port
            # thats why this code needs to run in a different thread
            data, address = self._server_socket.recvfrom(BUFFER_SIZE) 
            data = data.decode('utf-8')
            print('UnicastHandler: Received message from client: ', address)
            print('UnicastHandler: Message: ', data)

            if data:
                data = data.split(':')
                assert len(data) == 2, "There should not be a ':' in the message"
                messengerUUID = data[0]
                Middleware.addIpAdress(messengerUUID, address)# add this to list override if already present

                self.incommingUnicastHistory.append((data, address))
                for observer_func in self._listenerList:
                    observer_func(data[0], data[1]) 
                data[1] = None
               
    def subscribeUnicastListener(self, observer_func):
        self._listenerList.append(observer_func)

class BroadcastHandler():
    def __init__(self,UUID):
        self._UUID = UUID
        self.incommingBroadcastQ = Q()
        self.incommingBroadcastHistory = []
        self._listenerList = []

        self._broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Create a UDP socket for Listening
        self._listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Set the socket to broadcast and enable reusing addresses
        self._listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind socket to address and port
        self._listen_socket.bind((IP_ADRESS_OF_THIS_PC, BROADCAST_PORT))

        # Create Thread to listen to UDP Broadcast
        self._listen_UDP_Broadcast_Thread = threading.Thread(target=self._listenUdpBroadcast)
        self._listen_UDP_Broadcast_Thread.start()

    def broadcast(self, broadcast_message):
        # Send message on broadcast address
        self._broadcast_socket.sendto(str.encode(self._UUID + ':' + broadcast_message, encoding='utf-8'), (BROADCAST_IP, BROADCAST_PORT))
        #self.broadcast_socket.close()

    def subscribeBroadcastListener(self, observer_func):
        self._listenerList.append(observer_func)
    def _listenUdpBroadcast(self):
        print("listenUDP Broadcast Thread has started and not blocked Progress (by running in the background)")
        while True:
            # Code waits here until it recieves a unicast to its port
            # thats why this code needs to run in a different thread
            data, addr = self._listen_socket.recvfrom(BUFFER_SIZE)
            data = data.decode('utf-8')
            if data:
                messengerUUID = data.split(':')[0]
                Middleware.addIpAdress(messengerUUID,addr) # add this to list override if already present
                if messengerUUID != self._UUID:
                    print("Received broadcast message form",addr, ": ", data)
                    self.incommingBroadcastHistory.append((data, addr))
                    for observer_func in self._listenerList:
                        observer_func(data)
                data = None
