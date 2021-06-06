from dataclasses import dataclass

@dataclass(order=True)
class OrderedMessage:
    messageSeqNum: int
    messageCommand: str
    messageData: str

class HoldBackQ():
    def __init__(self):
        self._queue = list()
        self.lastDeliveredM = 0
    def append(self,x:OrderedMessage):
        self._queue.append(x)

        # Upon receiving agreed (final) priority
        #   – Mark message as deliverable
        #   – Reorder the delivery queue based on the priorities
        #   – Deliver any deliverable messages at the front of priority queue 

        sortedQ = sorted(self._queue)
        #print(sortedQ)
        for m in sortedQ:
            if m.messageSeqNum == self.lastDeliveredM+1:
                print(m)
                self._queue.remove(m)
                self.lastDeliveredM += 1
            else: 
                break


if __name__ == '__main__':
    # This is a Test
    hbQ = HoldBackQ()

    hbQ.append(OrderedMessage(2,'command', 'zweite nachricht'))
    hbQ.append(OrderedMessage(1,'command', 'erste nachricht'))
    hbQ.append(OrderedMessage(4,'command', 'vierte nachricht'))
    hbQ.append(OrderedMessage(3,'command', 'dritte nachricht'))
