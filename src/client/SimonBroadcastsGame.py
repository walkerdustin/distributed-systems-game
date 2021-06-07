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


states = {}                 # python dictionary {"key": value}
class Statemachine(): # there should be only one Instance of this class

    # State Storage, Parameters and Variables
    UUID = str(uuid.uuid4())
    players = PlayersList() 
    playerName = ''
    gameRoomPort = 61424
    currentState = ''

    simonSaysString = ''
    playersResponses = []


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

    @classmethod
    def switchStateTo(cls, toStateName):
        if "exit" in dir(states[cls.currentState]): # check if the state has a exit() function
            states[cls.currentState].exit() # execute the exit function
        if "entry" in dir(states[toStateName]): # check if the state has a entry() function
            states[toStateName].entry()
        cls.currentState = toStateName

    def __init__(self):
        self.middleware = Middleware(Statemachine.UUID, self)
        Statemachine.currentState = "Initializing"
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
            # call initiateVoting after use rinput
            # rawInput = input("want to vote? (v)")
            # if rawInput == 'v':
            #     self.middleware.initiateVoting()
            sleep(1)
            if len(self.players.playerList) <= 1:
                # only 1 player in list --> self 
                self.middleware.leaderUUID = self.UUID
                self.switchStateTo("simon_waitForPeers")
            else:
                self.switchStateTo("player_waitGameStart")
            
            # State Actions
            
            #Middleware.subscribeOrderedDeliveryQ(lambda x, y: print(f'Delivery Recieved!!!!!!!!!!!!!!!!!!!!!!!!!!! command {x}; data {y}'))
            
            # self.middleware.multicastOrderedReliable('command 1', 'number 1')
            # self.middleware.multicastOrderedReliable('command 2', 'number 2')
            # self.middleware.multicastOrderedReliable('command 3', 'number 3')
            # sleep(20)
            pass
        tempState.run = state_Lobby_f
        ############################################## Voting
        tempState = self.State("Voting")
        def state_voting_entry():
            print('Voting started')
        tempState.entry = state_voting_entry
        def state_voting_f():
            # When I'm Simon I start the voting
            if self.UUID == self.middleware.leaderUUID:
                self.middleware.initiateVoting()
            # else i'm doing nothing
            
        tempState.run = state_voting_f

        # SIMON STATES ###############################
        ############################################## waitForOtherPeers
        tempState = self.State("simon_waitForPeers")
        def state_simon_waitForPeers_entry():
            print("Simon: Waiting for players...\n")
        tempState.entry = state_simon_waitForPeers_entry

        def state_simon_waitForPeers_f():
            while len(self.players.playerList) < 2:
                Statemachine.switchStateTo("simon_startNewRound")
            
        tempState.run = state_simon_waitForPeers_f
        ############################################## startNewRound
        tempState = self.State("simon_startNewRound")
        def state_simon_startNewRound_f():
            # Simon starts a new round by declaring a new string
            self.simonSaysString = input("Simon: What do you want to Multicast?\n")
            self.middleware.multicastOrderedReliable('startNewRound', self.simonSaysString)
            print('multicastet: "' + self.simonSaysString + '" to all players')
            Statemachine.switchStateTo("simon_waitForResponses")
        tempState.run = state_simon_startNewRound_f
        ############################################## waitForResponses
        tempState = self.State("simon_waitForResponses")
        def state_simon_waitForResponses_entry():
            Middleware.subscribeOrderedDeliveryQ(self.collectPlayerInput_f)
        tempState.entry = state_simon_waitForResponses_entry
        def state_simon_waitForResponses_f():
            pass
        tempState.run = state_simon_waitForResponses_f
        def state_simon_waitForResponses_exit():
            Middleware.unSubscribeOrderedDeliveryQ(self.collectPlayerInput_f)
        tempState.exit = state_simon_waitForResponses_exit

        # PLAYER STATES ##############################
        ############################################## State 3
        tempState = self.State("player_waitGameStart")
        def state_player_waitGameStart_entry():
            print("Player: Waiting for game to start.\n")
            self.middleware.subscribeOrderedDeliveryQ(self.onReceiveGameStart_f)
            Middleware.subscribeOrderedDeliveryQ(self.collectPlayerInput_f)
        tempState.entry = state_player_waitGameStart_entry
        def state_player_waitGameStart_f():
            if self.simonSaysString != '':
                Statemachine.switchStateTo("player_playGame")
        tempState.run = state_player_waitGameStart_f
        ############################################## State 3
        tempState = self.State("player_playGame")
        def state_player_playGame_entry():
            playerInput = input("Input your game response.")
            self.middleware.multicastOrderedReliable("playerResponse", playerInput)
        tempState.entry = state_player_playGame_entry
        def state_player_playGame_f():
            pass
        tempState.run = state_player_playGame_f
        def state_player_playGame_exit():            
            self.middleware.unSubscribeOrderedDeliveryQ(self.onReceiveGameStart_f)
            Middleware.subscribeOrderedDeliveryQ(self.collectPlayerInput_f)
        tempState.exit = state_player_playGame_exit

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
    
    def onReceiveGameStart_f(self, messengerUUID, command, data):
        if command == 'startNewRound':
            self.simonSaysString = data
    
    def collectPlayerInput_f(self, messengerUUID, command, data):
            if command == 'playerResponse':
                if data == self.simonSaysString:
                    self.players.addPoints(messengerUUID, 10)
                    self.simonSaysString = ''
                    self.players.printLobby()
                    self.switchStateTo('Voting')


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
        