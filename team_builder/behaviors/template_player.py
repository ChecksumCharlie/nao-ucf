import sys
import time
from multiprocessing import Process

from util import nao_robot as robot
from util import parameters as param

class LogicFor:
    def __init__(self, RobotGiven):
        self.player = RobotGiven
        self.isRunning = True

    def __del__(self):
        self.isRunning = False

    def update(self):
        while (self.isRunning):
            param.wrapFSM(self)

    def runFSM(self):            

        if (True):
            print "This is my only state."
