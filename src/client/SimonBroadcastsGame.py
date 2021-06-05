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
# c:\Git_Repos\distributed-systems-game\src\client
# C:\Users\du-wa\AppData\Local\Programs\Python\Python39\python39.zip
# C:\Users\du-wa\AppData\Local\Programs\Python\Python39\DLLs
# C:\Users\du-wa\AppData\Local\Programs\Python\Python39\lib
# C:\Users\du-wa\AppData\Local\Programs\Python\Python39
# c:\Git_Repos\distributed-systems-game\venv
# c:\Git_Repos\distributed-systems-game\venv\lib\site-packages
# c:\Git_Repos\distributed-systems-game\venv\lib\site-packages\win32
# c:\Git_Repos\distributed-systems-game\venv\lib\site-packages\win32\lib
# c:\Git_Repos\distributed-systems-game\venv\lib\site-packages\Pythonwin
# c:\Git_Repos\distributed-systems-game\src                                     <----------
                                       
import uuid
from time import sleep
usleep = lambda x: sleep(x/1000_000.0) # sleep for x microseconds
from middleware.middleware import Middleware
import time
from client.Player import PlayersList


######################################  CONSTANTS
WAIT__MILLISECONDS_FOR_ANSWER = 1000

#constants/defines
# SUBNETMASK = "255.255.255.0"
# BROADCAST_PORT = 61425

# def enterGame(self, uuid):

#     # Send broadcast message
#     message = str(self.UUID) + ' at ' + IP_ADRESS_OF_THIS_PC + ' is looking for Simon.'
#     broadcast(BROADCAST_IP, self.BROADCAST_PORT, message)
#     print(message)
#     hostSocket.bind((IP_ADRESS_OF_THIS_PC, self.BROADCAST_PORT))

#     try:
#         print('Waiting for response...')
#         data, server = hostSocket.recvfrom(buffer_size)
#         print('Received message from server: ', data.decode())
#         # if str(data) == "is looking for Simon":
#         #     self.becomeSimon # + you take the first slot in ring
#         # elif str(data) == "i am Simon":
#         #     self.becomeOther # + next free spot in ring is no. xxx
#         # else:
#         #     self.RaiseError

#     except Exception as e:
#         print(e)
#     finally:
#         hostSocket.close()
#         print('Socket closed')
#     pass

states = {}                 # python dictionary {"key": value}
class Statemachine(): # there should be only one Instance of this class

    # State Storage, Parameters and Variables
    UUID = str(uuid.uuid4())
    players = PlayersList() 
    middleware = Middleware(UUID)
    playerName = ''
    gameRoomPort = 61424

    #players = [] # uuid s of all active players

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

    def switchStateTo(self, toStateName):
        if "exit" in dir(states[self.currentState]): # check if the state has a exit() function
            states[self.currentState].exit() # execute the exit function
        if "entry" in dir(states[toStateName]): # check if the state has a entry() function
            states[toStateName].entry()
        self.currentState = toStateName

    def __init__(self):
        self.currentState = "Initializing"
        ########################################################################### defining all states
        ############################################## Initializing
        tempState = self.State("Initializing")
        def state_initializing_f():
            # State Actions
            print("UUID is: ", self.UUID)
            print("sleeping for 1 second\n\n")
            sleep(1)
            self.playerName = input("Select Player Name: ")
            rawInput = input("Select Game Room Port: \nLeave empty for (Default: 61424)")
            self.gameRoomPort = (int(rawInput) if rawInput else 61424) #LOL, why can I write something like this? Python is hillarious! XD
            self.players.addPlayer(self.UUID,self.playerName)
            self.players.printLobby()
            # State Transition.
            if True:
                self.switchStateTo("Lobby")    # the self refers to the Statemashine (SM objekt)

        tempState.run = state_initializing_f # overriding the run() method of state0
        ############################################## Lobby
        tempState = self.State("Lobby")
        def state_Lobby_entry():
            #entry function
            command = 'enterLobby'
            data = self.playerName
            self.middleware.broadcastToAll(command,data)
            #self.StartWaitingTime = time.time_ns()
            print("entering Lobby...")
            ## get Lobby members
            self.middleware.subscribeBroadcastListener(self.respondWithPlayerList)
            self.middleware.subscribeUnicastListener(self.listenForPlayersList)
        tempState.entry = state_Lobby_entry
        ##########
        def state_Lobby_f():
            # State Actions
            
            # data = self.broadcastHandler.incommingBroadcastQ.pop()
            # if time.time_ns() + WAIT__MILLISECONDS_FOR_ANSWER * 1_000_000 > self.StartWaitingTime:
            #     self.switchStateTo("simon_startNewRound")
            # if data: # if I got a response
            #     self.switchStateTo("player_waitGameStart")
            #self.middleware._tcpUnicastHandler.se
            pass
        tempState.run = state_Lobby_f
        ############################################## Voting
        tempState = self.State("Voting")
        def state_voting_f():
            print('Voting started')
            # casual nodes just wait for new simon announcement
            # Simon: _initiatesVoting in middleware --> the rest is handled by the middleware
            self.middleware._initiateVoting(self)
            
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

    ################################################################# Observer functions
    def listenForPlayersList(self, messengerUUID:str, command:str, data:str):
        """This funcion recieves and decodes the message sent from the function respondWithPlayerList
        the List is severated by , and # 
        
        Args:
            message (str): message looks like this: PlayerList:e54aaddc-54fa-4484-a834-b56f10d55e65,p1,0#
            messengerUUID (str, optional): [description]. Defaults to None.
        """
        if command == 'PlayerList':
            #PlayerList:e54aaddc-54fa-4484-a834-b56f10d55e65,p1,0#
            playersList = data
            self.players.updateList(playersList)
        

    def respondWithPlayerList(self, messengerUUID:str, command:str, data:str):
        if command == 'enterLobby':
            self.middleware.sendIPAdressesto(messengerUUID)

            responseCommand = 'PlayerList'
            responseData = self.players.toString()
            self.middleware.sendMessageTo(messengerUUID, responseCommand, responseData)
            
            # add the asking player to my game List
            self.players.addPlayer(messengerUUID, data)
            self.players.printLobby()

if __name__ == '__main__':
    """
    This is the game
    """
    print("HELLO, this is Simon multicasts\n\n")
    print("the working Directory is:", os.getcwd())
    print("The used Python executable is: ", sys.executable)

    print("this is my process id: ", os.getpid())

    SM = Statemachine()
    while True:
        SM.runLoop()
        usleep(1) # put a sleep in the loop to not stress the cpu to much
        # with this 1 micro second sleep there is 0% cpu usage instead of 30%
        