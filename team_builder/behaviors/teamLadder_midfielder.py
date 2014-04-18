import sys
import time
from multiprocessing import Process

from util import nao_robot as robot
from util import parameters as param

class LogicFor:
    def __init__(self, RobotGiven):
        self.player = RobotGiven
        self.goalCheckTime = time.time()
        self.isRunning = True
        self.firstLoop = True

    def __del__(self):
        self.isRunning = False

    def update(self):
        while (self.isRunning):
            param.wrapFSM(self)

    def runFSM(self):  
            # new value
            RedBall = self.player.getRedBall()
            RedBall2 = self.player.getRedBall2()
            Enemy = self.player.getPinkPlayers()
            Goal = self.player.getYellowGoal()
            YellowHeight = self.player.getYellowGoalHeight()
            YellowWidth = self.player.getYellowGoalWidth()
            # behavior logic

            # shows that robots are active to viewers
            if (self.firstLoop==True):
                self.player.initStance()
                self.firstLoop=False

            # aid fall detection
            self.player.motionProxy.move(0, 0, 0)

            print RedBall2
            
            if (self.player.hasFallen()):
                self.player.initStance()
            
            # elif (YellowHeight > 120 or YellowWidth > 210):
            #     print "reached limit" + str(RedBall)
            #     if (len(RedBall)<=1):
            #         self.player.motionProxy.move(0, 0, 0.5)
            #     elif (RedBall[0]<260):
            #         self.player.motionProxy.move(0, 0, 0.05)
            #     elif (RedBall[0]>400):
            #         self.player.motionProxy.move(0, 0, -0.05)
            #     else:
            #         self.player.motionProxy.move(0, 0, 0)

            # No value from top camera -> wait
            elif (RedBall == None):
                pass
            
            # Red ball in top camera
            elif (len(RedBall)>1):
                if (RedBall[0]<300):
                    self.player.motionProxy.move(0.2, 0, 0.05)
                elif (RedBall[0]>340):
                    self.player.motionProxy.move(0.2, 0, -0.05)
                else:
                    self.player.motionProxy.move(0.2, 0, 0)
            
            # No value from bottom camera -> wait
            elif (RedBall2 == None):
                    pass
            
            # Red ball in bottom camera
            elif (len(RedBall2)>1):
                print "seeing ball bottom cam"
                if (RedBall2[1]>440):
                    if (Goal == []):
                        self.player.motionProxy.move(0, 0.5, -0.4)
                    elif(Goal[0]<300):
                        self.player.motionProxy.move(0, 0.5, -0.4)
                    elif (Goal[0]>340):
                        self.player.motionProxy.move(0, 0.5, -0.4)
                    else:
                        print "trying kick"
                        if (RedBall2[0]<=320):
                            self.player.killWalk()
                            self.player.rightKick(1.0, 1.7, 2.5)
                            self.player.walk2(0.1, 0, 0)
                        else:
                            self.player.killWalk()
                            self.player.leftKick(1.0, 1.7, 2.5)
                            self.player.walk2(0.1, 0, 0)
                # slow speed approach
                elif (RedBall2[0]<300 and RedBall2[1]>240):
                    self.player.walk2(0.1, 0.2, 0.1)
                elif (RedBall2[0]>340 and RedBall2[1]>240):
                    self.player.walk2(0.1, -0.2, -0.1)
                elif (RedBall2[1]>240):
                    self.player.walk2(0.1, 0, 0)
                # normal speed approach
                elif (RedBall2[0]<300):
                    self.player.walk2(0.5, 0.2, 0.1)
                elif (RedBall2[0]>340):
                    self.player.walk2(0.5, -0.2, -0.1)
                else:
                    self.player.walk2(0.5, 0, 0)

            else:
                print "not vis at all"
                ### .moveStop() does not halt .move(x, y, z)
                self.player.motionProxy.move(0, 0.5, -0.4)
