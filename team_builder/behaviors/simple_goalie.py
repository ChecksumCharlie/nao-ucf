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
            # new value
            RedBall = self.player.getRedBall()
            # behavior logic
            if (len(RedBall)>0):
                if (RedBall[0]<300):
                    self.player.sidestep(1.0)
                elif (RedBall[0]>400):
                    self.player.sidestep(-1.0)
                else:
                    self.player.sidestep(0.0)
            else:
                self.player.sidestep(0.0)
