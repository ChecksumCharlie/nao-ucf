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
            if (RedBall == None):
                pass
            elif (len(RedBall)>1):
                    # print RedBall[0]
                    if (RedBall[0]<300):
                        self.player.sidestep(0.2)
                    if (RedBall[0]>400):
                        self.player.sidestep(-0.2)
                    if (RedBall[0]<=400 and RedBall[0]>=300):
                        self.player.stop()


            else:
                RedBall = self.player.getRedBall2()
                if (RedBall == None):
                    pass
                elif (len(RedBall)>1):
                    if (RedBall[0]<300):
                        self.player.sidestep(0.2)
                    if (RedBall[0]>400):
                        self.player.sidestep(-0.2)
                    if (RedBall[1]>470 and RedBall[0]<=400 and RedBall[0]>=300):
                        self.player.rightKick(1.0, 1.4, 2.5)
                    if (RedBall[0]<=400 and RedBall[0]>=300):
                        self.player.stop()
                else: 
                    self.player.stop()

