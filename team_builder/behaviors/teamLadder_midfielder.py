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
            # behavior logic
            
            if (self.player.hasFallen()):
                self.player.initStance()

            elif (RedBall == None):
                pass
            
            elif (len(RedBall)>1):
                print "first cam vis"
                if (RedBall[0]<300):
                    self.player.motionProxy.move(0.2, 0, 0.05)
                elif (RedBall[0]>340):
                    self.player.motionProxy.move(0.2, 0, -0.05)
                else:
                    self.player.motionProxy.move(0.2, 0, 0)
            
            else:
                RedBall2 = self.player.getRedBall2()
                if (RedBall2 == None):
                    print "none in 2"
                elif (len(RedBall2)>1):
                    print "second cam vis"
                    if (RedBall2[0]<300):
                        self.player.motionProxy.move(0.2, 0.2, 0.1)
                    elif (RedBall2[0]>340):
                        self.player.motionProxy.move(0.2, -0.2, -0.1)
                    else:
                        self.player.motionProxy.move(0.2, 0, 0)

                else:
                    print "not vis at all"
                    ### .moveStop() does not halt .move(x, y, z)
                    self.player.motionProxy.move(0, 0, 0.2)
