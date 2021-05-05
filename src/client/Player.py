
class Player():
    def __init__(self,uuid,name,points=0):
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
            print("\nyou can't start the game yet wait for more players")
    
    def addPlayer(self, player:Player):
        self.playerList[player.uuid] += player
        self.printLobby()
    
    def addPlayer(self, uuid:str, name:str):
        self.playerList[uuid] = Player(uuid,name)
    
    def toString(self): # , , #
        s = ''
        for uuid, player in self.playerList.items():
            s += str(uuid)+','+str(player.name)+','+str(player.points)+'#'
        return s

    def updateList(self, playersList:str):
        players = playersList.split('#')
        for player in players:
            player = player.split(',')
            uuid = player[0]
            name = player[1]
            points = player[2]
            self.addPlayer(Player(uuid, name, points))
