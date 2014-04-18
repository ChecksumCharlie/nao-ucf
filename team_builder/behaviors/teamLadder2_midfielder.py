import sys
import time
from multiprocessing import Process

from util import nao_robot as robot
from util import parameters as param

class LogicFor:
    def __init__(self, RobotGiven):
        self.player = RobotGiven
        self.timeStep = time.time()
        self.isRunning = True
        
        self.nextState = "Init_Stance"

    def __del__(self):
        self.isRunning = False

    def update(self):
        while (self.isRunning):
            param.wrapFSM(self)

    def runFSM(self):  
            # new value
            self.RedBall = self.player.getRedBall()
            self.RedBall2 = self.player.getRedBall2()
            if (self.RedBall2 != None):
                if (len(self.RedBall2)>1):
                    self.RedBall = self.RedBall2

            self.Enemy = self.player.getPinkPlayers()
            self.Goal = self.player.getYellowGoal()
            self.GoalHeight = self.player.getYellowGoalHeight()
            self.GoalWidth = self.player.getYellowGoalWidth()
            # behavior logic

            # aid fall detection
            self.player.motionProxy.move(0, 0, 0)

            # fall recovery            
            if (self.player.hasFallen()):
                self.player.initStance()
            else:
                self.callState()
            
    def callState(self):

        print "State-> " + self.nextState

        if (self.RedBall == None or self.RedBall2 == None or self.Goal == None):
            pass

        elif (self.nextState == "Init_Stance"):
            self.stateInitStance()

        elif (self.nextState == "Ball_Search"):
            self.stateBallSearch()

        elif (self.nextState == "Ball_Seek"):
            self.stateBallSeek()

        elif (self.nextState == "Ball_Kick"):
            self.stateBallKick()

        elif (self.nextState == "Slow_Approach"):
            self.stateBallSeekSlow()

        elif (self.nextState == "Circle_Ball"):
            self.stateCircleBall()

        else:
            print "Not a valid state!"

    def stateInitStance(self):
        self.player.initStance()
        self.nextState = "Ball_Search"

    def stateBallSearch(self):
        if (len(self.RedBall)<1):
                self.player.motionProxy.move(0, 0.5, 0.5)
        else:
            self.nextState = "Ball_Seek"

    def stateBallSeek(self):
        # print self.RedBall
        
        if (len(self.RedBall)>1):
            if (self.RedBall[0]<300):
                self.player.motionProxy.move(1, 0, 0.05)
            elif (self.RedBall[0]>340):
                self.player.motionProxy.move(1, 0, -0.05)
            else:
                self.player.motionProxy.move(1, 0, 0)
           
        else:
            self.nextState = "Ball_Search"

        if (len(self.RedBall2)>1):

                if (self.RedBall2[1]>280):
                    self.player.killWalk()
                    self.nextState = "Slow_Approach"
                if (self.RedBall2[1]>440):
                    self.player.killWalk()
                    self.nextState = "Ball_Kick"



    def stateBallSeekSlow(self):
        if (len(self.RedBall2)>1):
            if (self.RedBall2[1]>440):
                self.player.killWalk()
                self.nextState = "Ball_Kick"
            elif (self.RedBall2[1]>350):
                if(self.Goal == []):
                    self.player.killWalk()
                    self.nextState = "Circle_Ball"
                elif(self.Goal[0]<300):
                    self.player.killWalk()
                    self.nextState = "Circle_Ball"
                elif(self.Goal[0]>340):
                    self.player.killWalk()
                    self.nextState = "Circle_Ball"

            elif (self.RedBall2[0]<300):
                self.player.walk2(0.1, 0.2, 0.1)
            elif (self.RedBall2[0]>340):
                self.player.walk2(0.1, -0.2, -0.1)
            else:
                self.player.walk2(0.1, 0, 0)

        else:
            self.player.killWalk()
            self.nextState = "Ball_Search"

    def stateBallKick(self):
        self.player.rightKick(1.0, 1.5, 2.5)
        if (time.time()-self.timeStep>10):
            self.nextState = "Ball_Search"

    def stateCircleBall(self):
        print self.Goal
        if (self.Goal == []):
            self.player.motionProxy.move(0, 0.3, -0.15)
        elif(self.Goal[0]<300):
            self.player.motionProxy.move(0, -0.1, -0.15)
        elif (self.Goal[0]>340):
            self.player.motionProxy.move(0, 0.1, -0.15)
        else:
            self.player.killWalk()
            self.nextState = "Ball_Search"
        


        # if (nextState == "Kick_Ball"):
        #     print "Kicking Ball"
