from __future__ import division
import sys
import time
import math
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

    def freePath(self, enemy_coords, range_low, range_high):
        if (enemy_coords == []):
            return True

        num_enemy = int(math.floor(len(enemy_coords)/2))

        for x in xrange(num_enemy):
            if (enemy_coords[2*x] > range_low and enemy_coords[2*x] < range_high):
                return False

        return True

    def isCongested(self, enemy_coords):
        if (enemy_coords == []):
            return False

        num_enemy = int(math.floor(len(enemy_coords)/2))

        return True

    def runFSM(self): 
        # new value
        RedBall = self.player.getRedBall()
        RedBall_lower = self.player.getRedBall2()
        Enemy = self.player.getBluePlayers()
        Goal = self.player.getBlueGoal()

        print "Ball: ", RedBall
        print "Ball(lower)", RedBall_lower
        print "Enemy: ", Enemy
        print "Goal: ", Goal
        # behavior logic



        if (self.player.hasFallen()):
            self.player.initStance()
            self.player.setHeadAngle(0, "HeadPitch")

        if (RedBall_lower == [] and RedBall == []):
            print "Trying to find ball."

            goal_position = False

            self.player.walk2(0.0, .75, .75)
        elif (RedBall != []):
            print "Ball in Distance.  Approaching"

            goal_position = False

            if (RedBall[0] == 320):
                theta = 0.0
            elif (RedBall[0] < 320):
                theta = math.atan((475 - RedBall[1])/(320 - RedBall[0])) - math.radians(90)
            else:
                theta = math.fabs(math.atan((475 - RedBall[1])/(RedBall[0] - 320))  - math.radians(90))

            if (theta < -1.0):
                theta = -1.0
            if (theta > 1.0):
                theta = 1.0
            print "Theta: ", -theta*0.2

            self.player.walk2(.75, 0.0,-theta*0.2)
        elif (RedBall_lower != []):
            print "Positioning time."

            if (Goal != []):
                print "Goal in sight"

                if (Goal[0] < 280 or Goal[0] > 360):
                    print "Time to shift"
                    if (Goal[0] < 305):
                        self.player.walk2(0.0, -0.5, .1)
                    else:
                        self.player.walk2(0.0, 0.5, -.1)
                else:
                    print "Moving towards kick"
                    if (RedBall_lower[1] <= 460):
                        if (RedBall_lower[0] == 320):
                            theta = 0.0
                        elif (RedBall_lower[0] < 320):
                            theta = math.atan((475 - RedBall_lower[1])/(320 - RedBall_lower[0])) - math.radians(90)
                        else:
                            theta = math.fabs(math.atan((475 - RedBall_lower[1])/(RedBall_lower[0] - 320))  - math.radians(90))

                        if (theta < -1.0):
                            theta = -1.0
                        if (theta > 1.0):
                            theta = 1.0
                        print "Theta: ", -theta*0.2

                        self.player.walk2(.2, 0.0,-theta*0.2)
                    else:
                        print "Kicking"

                        if (RedBall_lower[0] < 320):
                            self.player.killWalk()
                            self.player.leftKick(1.0, 1.1, 2.3)
                        else:
                            self.player.killWalk()
                            self.player.leftKick(1.0, 1.1, 2.3)


            else:
                self.player.walk2(0.0, 0.5, -0.1)
                    
                

        else:
            pass
