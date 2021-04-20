"""
This python script represents the game logic for the simon says game.
the points, the game state and all the nessecarry functions to compute anything related to the game are here!
"""

import uuid
from time import sleep
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


states = {}                 # python dictionary {"key": value}
class Statemachine(object): # there should be only one Instance of this class
    # states = {}                 # this is a class variable, it is consistent in every Instance (Object olf the same class)
                                # python dictionary {"key": value}
    # State Storage, Parameters and Variables
    PARAMETER = 42
    counterN = 0
    ###############################################   internal class
    class State: # there are multiple instances of this class
        total_Number_of_states = 0  # this is a class variable, it is consistent in every Instance (Object olf the same class)

        def __init__(self, name):
            self.name = name
            self.ID = self.total_Number_of_states
            self.total_Number_of_states += 1
            states[name] = self          #add this state (self) to the collection (dictionary) of states with the key being name 

        def run(self):
            pass
    ##############################################

    def __init__(self):
        self.currentState = "Initializing"
        ########################################################################### defining all states
        ############################################## State 0
        tempState = self.State("Initializing")
        def run0():
            # State Actions
            print("initializing....\n")
            sleep(1)
            print(".....")
            sleep(1)
            print(".....")
            # State Transition
            self.currentState = "Step 1"    # the self refers to the Statemashine (SM objekt)
        tempState.run = run0 # overriding the run() method of state0
        ############################################## State 1
        tempState = self.State("Step 1")
        def run1():
            # State Actions
            print("doing step one")
            # State Transition
            if(True):
                self.currentState = "Step 2"
        tempState.run = run1
        ############################################## State 2
        tempState = self.State("Step 2")
        def run2():
            print("doing step two .....n = ", self.counterN)
            self.counterN += 1
            if(self.counterN < 10): 
                self.currentState = "Step 1"
            else:
                self.currentState = "Finish"
        tempState.run = run2
        ############################################## State 3
        tempState = self.State("Finish")
        def run3():
            print("finished")
            sleep(2)
        tempState.run = run3
        ##############################################

    def runLoop(self):
        states[self.currentState].run() # run the current state

if __name__ == '__main__':
    SM = Statemachine()
    while True:
        SM.runLoop()