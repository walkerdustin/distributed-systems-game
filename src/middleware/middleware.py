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
    MY_UUID = '' # later changed in the init, it is here to define it as a class variable, so that it is accessable easyly 
    
    def __init__(self,UUID):
        Middleware.MY_UUID = UUID  
        self._broadcastHandler = BroadcastHandler()
        self._unicastHandler = UnicastHandler()
        self._unicastHandler.subscribeUnicastListener(self._updateAdresses)

    @classmethod
    def addIpAdress(cls, uuid, addr):
        cls.ipAdresses[uuid] = addr

    def broadcastToAll(self, command:str, data:str=''):
        self._broadcastHandler.broadcast(command+':'+data)
    
    def sendMessageTo(self, uuid:str, command:str, data:str=''): # unicast
        ipAdress = self.ipAdresses[uuid]
        self._unicastHandler.sendMessage(ipAdress, command+':'+data)
    
    def sendIPAdressesto(self,uuid):
        command='updateIpAdresses'
        s=''
        for uuid, (addr,port) in self.ipAdresses.items():
            s += uuid+','+str(addr)+','+str(port)+'#'
        self.sendMessageTo(uuid,command,s)

    def subscribeBroadcastListener(self, observer_func):
        """this function gets called every time there this programm recieves a broadcast message

        Args:
            observer_func ([type]): observer_function needs to have func(self, messengerUUID:str, command:str, data:str)
        """
        self._broadcastHandler.subscribeBroadcastListener(observer_func)
    def subscribeUnicastListener(self, observer_func):
        """this function gets called every time there this programm recieves a broadcast message

        Args:
            observer_func ([type]): observer_function needs to have func(self, messengerUUID:str, command:str, data:str)
        """
        self._unicastHandler.subscribeUnicastListener(observer_func)

    def _updateAdresses(self, messengerUUID:str, command:str, data:str):
        """this function recieves and decodes the IPAdresses List from the function 
        sendIPAdressesto(self,uuid)

        Args:
            command (str): function needs to check if this (unicast message) shall be handled by this function
            message (str): [description]
        """
        if command == 'updateIpAdresses':
            removedLastHashtag = data[0:-1] # everything, but the last character
            for addr in removedLastHashtag.split('#'):
                addrlist = addr.split(',')
                self.addIpAdress(addrlist[0], (addrlist[1], int(addrlist[2])))
                #                 uuid           ipadress           port of the unicastListener


class UnicastHandler():
    _serverPort = 0 # later changed in the init, it is here to define it as a class variable, so that it is accessable easyly 

    def __init__(self):
        # Create a UDP socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._server_socket.bind(('', 0)) # ('', 0) '' use the lokal IP adress and 0 select a random open port
        UnicastHandler._serverPort = self._server_socket.getsockname()[1] # returns the previously selected (random) port
        print("ServerPort = ",UnicastHandler._serverPort)
        self.incommingUnicastHistory = []
        self._listenerList = [] # observer pattern

        # Create Thread to listen to UDP unicast
        self._listen_UDP_Unicast_Thread = threading.Thread(target=self._listenUnicast)
        self._listen_UDP_Unicast_Thread.start()

    
    def sendMessage(self, addr, message:str):
        self._server_socket.sendto(str.encode(Middleware.MY_UUID + '_'+IP_ADRESS_OF_THIS_PC + '_'+str(UnicastHandler._serverPort)+'_'+message), addr)
        print('UnicastHandler: sent message: ', message,"\n\tto: ", addr)

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
            print('\t\tMessage: ', data)

            if data:
                data=data.split('_')
                messengerUUID = data[0]
                messengerIP = data[1]
                messengerPort = int(data[2])    # this should be the port where the unicast listener socket 
                                                #(of the sender of this message) is listening on
                assert address ==  (messengerIP, messengerPort)                              
                message=data[3]
                messageSplit= message.split(':')
                assert len(messageSplit) == 2, "There should not be a ':' in the message"
                messageCommand = messageSplit[0]
                messageData = messageSplit[1]
                Middleware.addIpAdress(messengerUUID, address)# add this to list override if already present
                # ^I dont know if I need to do that but it cant delete anything so .... whatever

                self.incommingUnicastHistory.append((message, address))
                for observer_func in self._listenerList:
                    observer_func(messengerUUID, messageCommand, messageData) 
                data[1] = None
               
    def subscribeUnicastListener(self, observer_func):
        self._listenerList.append(observer_func)

class BroadcastHandler():
    def __init__(self):
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

    def broadcast(self, broadcast_message:str):
        """Send message to the broadcast Port defined at lauch of the Programm

        Args:
            broadcast_message (str): needs to have the format  "command:data" (the data could be csv encode with , and #)
        """
        # Send message on broadcast address
        self._broadcast_socket.sendto(str.encode(Middleware.MY_UUID + '_'+IP_ADRESS_OF_THIS_PC + '_'+str(UnicastHandler._serverPort)+'_'+broadcast_message, encoding='utf-8'), (BROADCAST_IP, BROADCAST_PORT))
        #                                                                                                           ^this is the port where the _listen_UDP_Unicast_Thread ist listening on
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
                data=data.split('_')
                messengerUUID = data[0]
                messengerIP = data[1]
                messengerPort = int(data[2])    # this should be the port where the unicast listener socket 
                                                #(of the sender of this message) is listening on
                message=data[3]
                Middleware.addIpAdress(messengerUUID,(messengerIP, messengerPort)) # add this to list override if already present
                if messengerUUID != Middleware.MY_UUID:
                    print("Received broadcast message form",addr, ": ", message)
                    message=data[3]
                    messageSplit= message.split(':')
                    assert len(messageSplit) == 2, "There should not be a ':' in the message"
                    messageCommand = messageSplit[0]
                    messageData = messageSplit[1]
                    self.incommingBroadcastHistory.append((messengerUUID, message))
                    for observer_func in self._listenerList:
                        observer_func(messengerUUID, messageCommand, messageData)
                data = None
