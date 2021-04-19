"""
Here are all the sockets.
There shall not be any sockets outside of this file.

There shall be one socket in one seperate thread (multithreading)
for every tcp connections
also one socket in a thread for the udp socket for broadcast
"""

import threading
import socket



class Middleware():
    holdBackQueue = []
    def __init__(self):
        pass



    def broadcastToAll(self, message):
        pass
    

    def sendMessageTo(self, uuid, message):
        pass