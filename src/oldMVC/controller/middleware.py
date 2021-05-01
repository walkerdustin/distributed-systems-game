"""
Here are all the sockets.
There shall not be any sockets outside of this file.

There shall be one socket in one seperate thread (multithreading)
for every tcp connections
also one socket in a thread for the udp socket for broadcast
"""

import threading
import socket
from time import sleep
usleep = lambda x: sleep(x/1000_000.0) # sleep for x microseconds

######################################### PARAMETER Constants
BROADCAST_PORT = 61425
BUFFER_SIZE = 1024
BROADCAST_LISTENER_SLEEP = 10 # microseconds

IP_ADRESS_OF_THIS_PC = socket.gethostbyname(socket.gethostname())
net = ipaddress.IPv4Network(IP_ADRESS_OF_THIS_PC + '/' + self.SUBNETMASK, False)
BROADCAST_IP = net.broadcast_address.exploded


class BroadcastHandler():
    def __init__(self):
        
        self.listenerList = []

        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Create a UDP socket for Listening
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Set the socket to broadcast and enable reusing addresses
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind socket to address and port
        self.listen_socket.bind((IP_ADRESS_OF_THIS_PC, BROADCAST_PORT))

        # Create Thread to listen to UDP Broadcast
        listen_UDP = threading.Thread(target=self.listenUdp)
        listen_UDP.start()
        print("listenUDP Thread has started and not blocked Progress (by running in the background")

    def broadcast(self, broadcast_message):
        
        # Send message on broadcast address
        self.broadcast_socket.sendto(str.encode(broadcast_message), (BROADCAST_IP, BROADCAST_PORT))
        #self.broadcast_socket.close()

    def subscribeBroadcastListener(self, observer):
        self.listenerList += observer
    def listenUdp(self):
        while True:
            data, addr = self.listen_socket.recvfrom(BUFFER_SIZE)
            usleep(BROADCAST_LISTENER_SLEEP)# sleep microseconds
            if data:
                print("Received broadcast message form",addr, ": ", data.decode())
    	        for observer in self.listenerList:
                    observer.broadcastMessageReceived()
                data = None



class Middleware():
    holdBackQueue = []
    deliveryQueue = []
        
    def __init__(self):
        broadcastHandler = BroadcastHandler()
        pass

    

    def broadcastToAll(self, message):
        pass
    

    def sendMessageTo(self, uuid, message):
        pass

