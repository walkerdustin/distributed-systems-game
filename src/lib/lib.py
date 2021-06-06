from dataclasses import dataclass


@dataclass(order=True)
class OrderedMessage:
    messageSeqNum: int
    messageCommand: str
    messageData: str
    messageID:str
    deliverable:bool

class HoldBackQ():
    def __init__(self):
        self._queue = list()
    def append(self,x:OrderedMessage):
        self._queue.append(x)

        # Upon receiving agreed (final) priority
        #   – Mark message as deliverable
        #   – Reorder the delivery queue based on the priorities
        #   – Deliver any deliverable messages at the front of priority queue 
        self.checkForDeliverables()
    
    def updateData(self, messageID:str, messageSeqNum:int, messageCommand:str, messageData:str):
        #find Messagewith message ID
        # set messageSeqNum
        # set messageCommand
        # set messageData
        # setDeliverableTrue
        
        for m in self._queue:
            if m.messageID == messageID:
                m.messageSeqNum = messageSeqNum
                m.messageCommand = messageCommand
                m.messageData = messageData
                m.deliverable = True
                break

        self.checkForDeliverables()

    def checkForDeliverables(self):
        # sort Q
        # check if message with lowest ID is deliverable
        # deliver this message
        sortedQ = sorted(self._queue)
        for m in sortedQ:
            if m.deliverable:
                for observer_func in Middleware.orderedReliableMulticast_ListenerList:
                    observer_func(m.messageCommand, m.messageData)
            else:
                break
        



if __name__ == '__main__':
    # This is a Test
    hbQ = HoldBackQ()

    hbQ.append(OrderedMessage(2,'command', 'zweite nachricht'))
    hbQ.append(OrderedMessage(1,'command', 'erste nachricht'))
    hbQ.append(OrderedMessage(4,'command', 'vierte nachricht'))
    hbQ.append(OrderedMessage(3,'command', 'dritte nachricht'))
