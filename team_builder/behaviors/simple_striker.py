from __future__ import division
import sys
import time
import math
from multiprocessing import Process

from util import nao_robot as robot

class LogicFor:
    def __init__(self, RobotGiven):
        self.player = RobotGiven

    def update(self):
            # new value
            RedBall = self.player.getRedBall()
            Enemy = self.player.getPinkPlayers()
            Goal = self.player.getBlueGoal()

            print "Ball: ", RedBall
            print "Enemy: ", Enemy
            print "Goal: ", Goal
            # behavior logic
            time.sleep(0.3)
            if (RedBall != [] and  Enemy == [] and Goal != []):
                print "No enemy, goal in sight."

                if (RedBall[1] > 450):
                	print "Adjusting sight."
                	self.player.killWalk()
                	angles = self.player.getAngle("Head")

                	if (math.degrees(angles[0]) == 0):
                		self.player.setHeadAngle(20, "HeadPitch")
                	else:
                		self.player.setHeadAngle(30, "HeadPitch")


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
                print "Theta: ", -theta*.02

                self.player.walk(-theta*0.2)
            elif (RedBall != [] and Enemy != [] and Goal != []):
                print "All three variables in sight."

                if (RedBall[1] > 450):
                	print "Adjusting sight."
                	self.player.killWalk()
                	angles = self.player.getAngle("Head")

                	if (math.degrees(angles[0]) == 0):
                		self.player.setHeadAngle(20, "HeadPitch")
                	else:
                		self.player.setHeadAngle(30, "HeadPitch")


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
                print "Theta: ", -theta*.02

                self.player.walk(-theta*0.2)
            elif (RedBall != [] and Enemy != [] and Goal == []):
                print "Time to defend, no goal in sight."
            elif (RedBall == [] and Enemy != [] and Goal != []):
                print "Cannot find ball, enemy and goal in sight. Relocating."
            else:
                self.player.killWalk()
                print "Other case."
