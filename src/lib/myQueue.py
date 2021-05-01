from collections import  deque
class Q():
    def __init__(self):
        self._queue = deque()
    def append(self,x):
        self._queue.append(x)
    def pop(self):
        try:
            return self._queue.popleft()
        except IndexError:
            return None