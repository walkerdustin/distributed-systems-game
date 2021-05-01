"""
This is just a terminal application that
(for now)
"""

from os import getpid
from time import sleep

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))    # this adds the src folder to the path # now you can import stuff
from controller.gameController import GameController
from controller import gameController

if __name__ == '__main__':
    """this is the terminal application that
    output is displayed here;
    user input here is forwarded to the controller
    """
    print("HELLO, this is Simon multicasts\n\n")

    print("this is my process id: ", getpid())

    GameController.start()

    # print("sleeping for 10 seconds\n\n")
    # sleep(10)

def showWaitingForPlayers():
    print("Waiting for Players to join the Game ... \n")

def showFoundAPlayer():
    print("FOUND a player")
    print("You are now the Simon!")

def showGetSimonInput():
    SimonSaid = input("You (Simon) say: ")



