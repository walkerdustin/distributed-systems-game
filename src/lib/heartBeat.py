import subprocess
from typing import OrderedDict

def findNeighbor(ownUUID, playerList):
    # only to be called if we don't yet have the neighbor
    # make ordered dict - uuid remains dict key
    ordered = sorted(playerList.playerList.keys())
    
    ownIndex = ordered.index(ownUUID)
    # add neighbor with smaller uuid
    if ordered[ownIndex + 1] and ordered[ownIndex + 1] != ownUUID:
        # another uuid exists and it's not our own
        return ordered[ownIndex+1]