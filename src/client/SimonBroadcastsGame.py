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

# For None-blocking keyboard input (just for windows)
import msvcrt

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
        # print("___________Switch State to ", toStateName)

    def __init__(self):
        self.middleware = Middleware(Statemachine.UUID, self)
        Statemachine.currentState = "Initializing"
        ########################################################################### defining all states
        ############################################## Initializing
        tempState = self.State("Initializing")
        def state_initializing_f():
            # State Actions
            print("UUID is: ", Middleware.MY_UUID)
            #print("sleeping for 1 second\n\n")
            #sleep(1)
            flush_input()
            self.playerName = input("Select Player Name: ")
            rawInput = input("\nSelect Game Room Port: \nLeave empty for (Default: 61424)")
            self.gameRoomPort = (int(rawInput) if rawInput else 61424) #LOL, why can I write something like this? Python is hillarious! XD
            self.players.addPlayer(Middleware.MY_UUID,self.playerName)
            #self.players.printLobby()
            # State Transition.
            if True:
                self.switchStateTo("Lobby")    # the self refers to the Statemashine (SM objekt)

        tempState.run = state_initializing_f # overriding the run() method of state0
        ############################################## Lobby
        tempState = self.State("Lobby")
        def state_Lobby_entry():
            # I assume, that I am the only one in this room
            # Therefore I assume, that I am the Leader
            self.middleware.leaderUUID = Middleware.MY_UUID
            # If I am not the first one in this lobby, I will get a response from the leader,
            # after I Broadcast "enter Lobby"
            # Leader UUID is then set in listenForPlayerList, as only the leader sends 'playerList'

            # these two need to be first, else -> Race condition
            self.middleware.subscribeBroadcastListener(self.respondWithPlayerList)
            self.middleware.subscribeTCPUnicastListener(self.listenForPlayersList)


            #entry function
            command = 'enterLobby'
            data = self.playerName
            self.middleware.broadcastToAll(command,data)
            #self.StartWaitingTime = time.time_ns()
            
        tempState.entry = state_Lobby_entry
        ##########
        def state_Lobby_f():
            # call initiateVoting after use rinput
            # rawInput = input("want to vote? (v)")
            # if rawInput == 'v':
            #     self.middleware.initiateVoting()
            
            sleep(0.5) #sleep a 500 ms
            if self.middleware.leaderUUID == Middleware.MY_UUID:
                self.switchStateTo("simon_waitForPeers")
            else:
                self.switchStateTo("player_waitGameStart")
            
        tempState.run = state_Lobby_f
        ############################################## Voting
        tempState = self.State("Voting")
        def state_voting_entry():
            print('Voting started')
            # When I'm Simon I start the voting
            if Middleware.MY_UUID == self.middleware.leaderUUID:
                self.middleware.leaderUUID = ''
                self.middleware.initiateVoting()
            # else i'm doing nothing
        tempState.entry = state_voting_entry
        def state_voting_f():
            if Middleware.MY_UUID == self.middleware.leaderUUID:
                Statemachine.switchStateTo("simon_waitForPeers")
            else:
                Statemachine.switchStateTo("player_waitGameStart")
        tempState.run = state_voting_f

        # SIMON STATES ###############################
        ############################################## simon_waitForPeers
        tempState = self.State("simon_waitForPeers")
        def state_simon_waitForPeers_entry():
            if len(self.players.playerList) < 3:
                print("Simon: Waiting for players...")
                print("At least 3 Players are needed to play the game")
        tempState.entry = state_simon_waitForPeers_entry

        def state_simon_waitForPeers_f():
            if len(self.players.playerList) >= 3: # if there are 3 or more players in the lobby
                Statemachine.switchStateTo("simon_startNewRound")
            
        tempState.run = state_simon_waitForPeers_f
        ############################################## simon_startNewRound
        tempState = self.State("simon_startNewRound")
        def state_simon_startNewRound_f():
            # Simon starts a new round by declaring a new string
            flush_input()
            self.simonSaysString = input("\nSimon: What do you want to Multicast?\n")
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
        ############################################## player_waitGameStart
        tempState = self.State("player_waitGameStart")
        def state_player_waitGameStart_entry():
            print("Player: Waiting for game to start.\n")
            Middleware.subscribeOrderedDeliveryQ(self.onReceiveGameStart_f)
            Middleware.subscribeOrderedDeliveryQ(self.collectPlayerInput_f)
        tempState.entry = state_player_waitGameStart_entry
        def state_player_waitGameStart_f():
            if self.simonSaysString != '':
                Statemachine.switchStateTo("player_playGame")
            elif self.middleware.leaderUUID == Middleware.MY_UUID:
                Statemachine.switchStateTo("simon_waitForPeers")
        tempState.run = state_player_waitGameStart_f
        ############################################## player_playGame
        tempState = self.State("player_playGame")
        def state_player_playGame_entry():
            #playerInput = input("\nInput your game response.\n")
            print("Simon said: ", self.simonSaysString)
            print("Type your response: ")
            self.playerInput = ''
            self.player_playGame_InputDone = False
            flush_input()
        tempState.entry = state_player_playGame_entry
        def state_player_playGame_f():
            if not self.player_playGame_InputDone:
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode("utf-8")
                    if key == '\r': # == Enter
                        self.middleware.multicastOrderedReliable("playerResponse", self.playerInput)
                        self.player_playGame_InputDone = True 
                    else:
                        self.playerInput += key
                        print(key, end='') # print without a newline

        tempState.run = state_player_playGame_f
        def state_player_playGame_exit():            
            Middleware.unSubscribeOrderedDeliveryQ(self.onReceiveGameStart_f)
            Middleware.subscribeOrderedDeliveryQ(self.collectPlayerInput_f)
        tempState.exit = state_player_playGame_exit

    def runLoop(self):
        states[self.currentState].run() # run the current state

    ################################################################# Observer functions
    def listenForPlayersList(self, messengerUUID:str, messengerSocket, command:str, playersList:str):
        """This funcion recieves and decodes the message sent from the function respondWithPlayerList
        the List is severated by , and # 
        
        Args:
            message (str): message looks like this: PlayerList:e54aaddc-54fa-4484-a834-b56f10d55e65,p1,0#
            messengerUUID (str, optional): [description]. Defaults to None.
        """
        if command == 'PlayerList':
            #PlayerList:e54aaddc-54fa-4484-a834-b56f10d55e65,p1,0#

            # I know that only the leader sends the player list
            # this means, that messengerUUID has to be the leader
            self.middleware.leaderUUID = messengerUUID

            self.players.updateList(playersList)

    def respondWithPlayerList(self, messengerUUID:str, command:str, playerName:str):
        # only the leader responds with this list
        if command == 'enterLobby':
            # add the asking player to my game List
            self.players.addPlayer(messengerUUID, playerName)
            # self.players.printLobby()
            if Middleware.MY_UUID == self.middleware.leaderUUID:
                self.middleware.sendIPAdressesto(messengerUUID)

                responseCommand = 'PlayerList'
                responseData = self.players.toString()
                self.middleware.sendTcpMessageTo(messengerUUID, responseCommand, responseData)
    
    def onReceiveGameStart_f(self, messengerUUID, command, data):
        if command == 'startNewRound':
            self.simonSaysString = data
    
    def collectPlayerInput_f(self, messengerUUID, command, data):
            if command == 'playerResponse':
                if data == self.simonSaysString:
                    self.players.addPoints(messengerUUID, 10)
                    self.simonSaysString = ''
                    self.players.printLobby()
                    self.switchStateTo("Voting")

def flush_input(): # flush the input buffer
    try: # for windows
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError: # for linux/unix
        import sys, termios    
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

if __name__ == '__main__':
    """
    This is the game
    """
    print("HELLO, this is Simon multicasts\n\n")
    #print("the working Directory is:", os.getcwd())
    #print("The used Python executable is: ", sys.executable)

    #print("this is my process id: ", os.getpid())

    SM = Statemachine()
    while True:
        SM.runLoop()
        usleep(1) # put a sleep in the loop to not stress the cpu to much
        # with this 1 micro second sleep there is 0% cpu usage instead of 30%
        