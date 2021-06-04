import subprocess
from typing import OrderedDict


class HeartBeat(): # there should only be one instance of this class
    neighborHosts = []

    def __init__(self):
        pass
    
    def addNeighbor(self, newNeighbor):
        self.neighborHosts.append(newNeighbor)
        print("neighbors :\n", self.neighborHosts)
        pass

    def removeNeighbor(self, rmNeighbor):
        self.neighborHosts.remove(rmNeighbor)
        print("neighbors :\n", self.neighborHosts)
        pass

    def findNeighbor(self, ownUUID, playerList):
        # go back if we already have assigned neighbors
        if len(self.neighborHosts) >= 2 or not playerList:
            return
        # make ordered dict - uuid remains dict key
        ordered = sorted(playerList.playerList.keys())
        # print("ordered Playerlist:\n")
        # for item in ordered:
        #     print(item)
        
        ownIndex = ordered.index(ownUUID)
        # add neighbor with smaller uuid
        if ownIndex + 1 < len(ordered):
            if ordered[ownIndex + 1] not in self.neighborHosts and not ownUUID:
                self.addNeighbor(ordered[ownIndex+1])
        else:
            if ordered[0] not in self.neighborHosts and not ownUUID:
                self.addNeighbor(ordered[0])
        
        # add neighbor with bigger uuid
        if ownIndex > 0:
            if ordered[ownIndex - 1] not in self.neighborHosts and not ownUUID:
                self.addNeighbor(ordered[ownIndex - 1])
        else:
            if ordered[len(ordered) - 1] not in self.neighborHosts and not ownUUID:
                self.addNeighbor(ordered[len(ordered) - 1])
        pass

    def sendHeartBeat(self):
        print("pinging neighbors\n")
        for neighbor in self.neighborHosts:
            ping = subprocess.Popen(   
                ["ping", "-n","10", neighbor],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
            )
            out, error = ping.communicate()
            print(out)
            print("\n\n")
            # TODO: catch erroneous cases and return to caller or handle them
            return out,error