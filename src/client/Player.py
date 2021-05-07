
class Player():
    def __init__(self,uuid,name,points):
        self.uuid = uuid
        self.name = name
        self.points = points
class PlayersList():
    def __init__(self):
        self.playerList = {} # {uuid: Player}
    
    def printLobby(self):
        print("GAME LOBBY".center(40,'_'))
        for uuid, player in self.playerList.items():
            print('{:<30}'.format(player.name), " | ", player.points)
        if len(self.playerList)<=1:
            print("\nyou can't start the game yet, wait for more players")
        else:
            print("Press 'ü' to enter the game \n someone needs to implement this part")
            # this might be an issue though, because mabe if you write input() you block this thread?
            # but maybe this is not an issue, because the architecture I have used is very nice!!!??? 
    
    def addPlayer(self, uuid:str, name:str, points:int = 0):
        self.playerList[uuid] = Player(uuid,name, points)
    
    def toString(self): # , , #
        s = ''
        for uuid, player in self.playerList.items():
            s += str(uuid)+','+str(player.name)+','+str(player.points)+'#'
        return s

    def updateList(self, playersList:str):
        """decodes the PlayersList string recieved via unicast

        Args:
            playersList (str): message looks like this: PlayerList:e54aaddc-54fa-4484-a834-b56f10d55e65,p1,0#
        """
        assert playersList[-1] =='#', f"the last character should be a #, maybe the string: {playersList} is empty"
        players = playersList.split('#')[0:-1] # split by the # (csv-style) and remove the last hashtag
        for player in players:
            player = player.split(',')
            uuid = player[0]
            name = player[1]
            points = player[2]
            self.addPlayer(uuid, name, points)
        self.printLobby()
