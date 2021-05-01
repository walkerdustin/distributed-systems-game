
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))    # this adds the src folder to the path # now you can import stuff
from controller.gameController import GameController
from library.singletonDecorator import singleton


@singleton
class GameController():
    pass