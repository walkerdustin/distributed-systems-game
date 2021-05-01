"""
This python script represents the game logic for the simon says game.
the points, the game state and all the nessecarry functions to compute anything related to the game are here!
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))    # this adds the src folder to the path # now you can import stuff
# add to path # get parent directory        #get absolut path of # this python file

# the path looks like this now: python looks here vor .py files
# for p in sys.path:
#     print(p)
# c:\Git_Repos\distributed-systems-game\src\model
# C:\Users\du-wa\AppData\Local\Programs\Python\Python39\python39.zip
# C:\Users\du-wa\AppData\Local\Programs\Python\Python39\DLLs
# C:\Users\du-wa\AppData\Local\Programs\Python\Python39\lib
# C:\Users\du-wa\AppData\Local\Programs\Python\Python39
# c:\Git_Repos\distributed-systems-game\venv
# c:\Git_Repos\distributed-systems-game\venv\lib\site-packages
# c:\Git_Repos\distributed-systems-game\venv\lib\site-packages\win32
# c:\Git_Repos\distributed-systems-game\venv\lib\site-packages\win32\lib
# c:\Git_Repos\distributed-systems-game\venv\lib\site-packages\Pythonwin
# c:\Git_Repos\distributed-systems-game\src                                         <----------

import uuid
import socket
import ipaddress
from broadcastSender import broadcast
from time import sleep
from controller.middleware import Middleware
from library.singletonDecorator import singleton

@singleton
class SimonBroadcastsGame():
    #constants/defines
    SUBNETMASK = "255.255.255.0"
    BROADCAST_PORT = 61425

    def __init__(self):
        self.UUID = uuid.uuid4()
        self.enterGame(self.UUID)
        pass

    def enterGame(self, uuid):
        
        hostSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        IP_ADRESS_OF_THIS_PC = socket.gethostbyname(socket.gethostname())
        net = ipaddress.IPv4Network(IP_ADRESS_OF_THIS_PC + '/' + self.SUBNETMASK, False)
        BROADCAST_IP = net.broadcast_address.exploded
        buffer_size = 1024

        # Send broadcast message
        message = str(self.UUID) + ' at ' + IP_ADRESS_OF_THIS_PC + ' is looking for Simon.'
        broadcast(BROADCAST_IP, self.BROADCAST_PORT, message)
        print(message)
        hostSocket.bind((IP_ADRESS_OF_THIS_PC, self.BROADCAST_PORT))

        try:
            print('Waiting for response...')
            data, server = hostSocket.recvfrom(buffer_size)
            print('Received message from server: ', data.decode())
            # if str(data) == "is looking for Simon":
            #     self.becomeSimon # + you take the first slot in ring
            # elif str(data) == "i am Simon":
            #     self.becomeOther # + next free spot in ring is no. xxx
            # else:
            #     self.RaiseError

        except Exception as e:
            print(e)
        finally:
            hostSocket.close()
            print('Socket closed')
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
        ############################################## Initializing
        tempState = self.State("Initializing")
        def state_initializing_f():
            # State Actions
            print("UUID calculation happens here.")
            
            # State Transition
            self.currentState = "Idle"    # the self refers to the Statemashine (SM objekt)
        tempState.run = state_initializing_f # overriding the run() method of state0
        ############################################## Idle
        tempState = self.State("Idle")
        def state_idle_f():
            # State Actions
            print("Broadcast message and wait for response.")
            # State Transition: according to response (t/o 3sec).
            # if SimonAlreadyExists:
            #     self.currentState = "player_waitGameStart"
            # elif ThereIsNoSimonYet:
            #     self.currentState = "simon_startNewRound"
        tempState.run = state_idle_f
        ############################################## Voting
        tempState = self.State("Voting")
        def state_voting_f():
            print("run voting procedure with other hosts")
            # if IGotElectedAsSimon:
            #     self.currentState = "simon_waitForPeers"
            # elif OtherPlayerGotElected:
            #     self.currentState = "player_waitGameStart"
        tempState.run = state_voting_f

        # SIMON STATES ###############################
        ############################################## waitForOtherPeers
        tempState = self.State("simon_waitForPeers")
        def state_simon_waitForPeers_f():
            print("Wait for User to input string of chars.")
            print("Multicast string of chars to others.")
            self.currentState = "simon_startNewRound"
        tempState.run = state_simon_waitForPeers_f
        ############################################## startNewRound
        tempState = self.State("simon_startNewRound")
        def state_simon_startNewRound_f():
            print("Wait for User to input string of chars.")
            print("Multicast string of chars to others.")
            self.currentState = "simon_waitForResponses"
        tempState.run = state_simon_startNewRound_f
        ############################################## waitForResponses
        tempState = self.State("simon_waitForResponses")
        def state_simon_waitForResponses_f():
            print("Wait for other peer's game round input responses with t/o.")
            # if allPeersResponded or timeoutReached:
            #     print("Evaluate the winner if everyone responded OR timeout reached.")
            #     print("Multicast to every round participant the updated scoreboard.")
            #     self.currentState = "Voting"
        tempState.run = state_simon_waitForResponses_f

        # PLAYER STATES ##############################
        ############################################## State 3
        tempState = self.State("player_waitGameStart")
        def state_player_waitGameStart_f():
            print("Receive multicast message from Simon containing the string.")
            self.currentState = "player_playGame"
        tempState.run = state_player_waitGameStart_f
        ############################################## State 3
        tempState = self.State("player_playGame")
        def state_player_playGame_f():
            print("Wait for User to input string of chars and add timestamp.")
            print("Unicast string of chars to Simon.")
            self.currentState = "player_awaitSimonResponse"
        tempState.run = state_player_playGame_f
        ############################################## State 3
        tempState = self.State("player_awaitSimonResponse")
        def player_awaitSimonResponse():
            print("Update and print own copy of global score board.")
            self.currentState = "Voting"
        tempState.run = player_awaitSimonResponse

    def runLoop(self):
        states[self.currentState].run() # run the current state

if __name__ == '__main__':
    host = SimonBroadcastsGame()
    SM = Statemachine()
    while True:
        SM.runLoop()