import sys
import time
from multiprocessing import Process

from util import nao_robot as robot
from util import parameters as param

class LogicFor:
    def __init__(self, RobotGiven):
        self.player = RobotGiven

    def update(self):
        
        param.wrapFSM(self)


    def runFSM(self): 
            # new value
            RedBall = self.player.getRedBall()
            RedBall2 = self.player.getRedBall2()

            # behavior logic
            if (len(RedBall)>0):
                if (len(RedBall2)>1):
                    if (RedBall2[1]>440):
                        self.player.rightKick(1.0, 1.9, 2.5)
                elif (RedBall[0]<300):
                    self.player.sidestep(1.0)
                elif (RedBall[0]>400):
                    self.player.sidestep(-1.0)
                else:
                    self.player.sidestep(0.0)
            else:
                self.player.sidestep(0.0)
