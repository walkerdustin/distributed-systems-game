"""
This python script represents the game logic for the simon says game.
the points, the game state and all the nessecarry functions to compute anything related to the game are here!
"""

import uuid

class SimonBroadcastsGame():
    """
    states:
    uninitialized: start 
    idle
    election
    inGame
    Error


    """
    def __init__(self):
        self.UUID = uuid.uuid4()
        self.enterGame(self.UUID)
        



    def enterGame(self, uuid):
        # broadcast( hello, is somebody there, my uuid is: )
        # if yes:
        #   if game running:
        #       wait until next round
        #   
        # if noAnswer:
        #   beLeaderSimon()
        #   waitForOther()
        pass

