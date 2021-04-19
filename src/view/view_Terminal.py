"""
This is just a terminal application that
(for now)
"""

from os import getpid
from time import sleep

if __name__ == '__main__':
    """this is the terminal application that
    output is displayed here;
    user input here is forwarded to the controller
    """
    print("HELLO, this is Simon multicasts\n\n")

    print("this is my process id: ", getpid())

    print("sleeping for 10 seconds\n\n")
    sleep(10)
