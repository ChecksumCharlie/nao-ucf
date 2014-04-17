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

    def update(self):
        param.wrapFSM(self)

    def freePath(self, enemy_coords):
        if (enemy_coords == []):
            return False

        num_enemy = int(math.floor(len(enemy_coords)/2))

        for x in xrange(num_enemy):
            if (enemy_coords[2*x] > 290 and enemy_coords[2*x] < 360):
                return True

        return False

    def runFSM(self): 
        # new value
        RedBall = self.player.getRedBall()
        RedBall_lower = self.player.getRedBall2()
        Enemy = self.player.getPinkPlayers()
        Goal = self.player.getBlueGoal()

        print "Ball: ", RedBall
        print "Ball(lower)", RedBall_lower
        print "Enemy: ", Enemy
        print "Goal: ", Goal
        # behavior logic


        if (self.player.hasFallen()):
            self.player.initStance()
            self.player.setHeadAngle(0, "HeadPitch")

        if (RedBall == [] and Goal != [] and RedBall_lower != []):
            print "Positioning"
            
            if (Goal[0] < 305):#shift and roate right
                self.player.walk2(0.0, 0.1, 0.1)
            elif (Goal[0] > 335):#Shift and rotate left
                self.player.walk2(0.0, -0.1, -0.1)
            else:
                pass

            if (Goal[0] >= 310 and Goal[0] <= 330):  
                if(self.freePath(Enemy)):#path blocked
                    print "Path Blocked."
                    self.player.stop()
                    
                    while (True):
                        RedBall_lower = self.player.getRedBall2()
                        if (RedBall_lower == []):
                            break
                        if (self.freePath(Enemy)):#shift and roate right
                            self.player.walk2(0.0, 0.1, 0.1)
                        else:
                            pass


                    if(RedBall_lower != []):
                        while(True):
                                RedBall_lower = self.player.getRedBall2()
                                print "In position Loop (Blocked)"
                                if(RedBall_lower[1] >=470 or RedBall_lower == []):
                                    self.player.killWalk()
                                    break
                                if (RedBall_lower[0] == 305):
                                    theta = 0.0
                                elif (RedBall_lower[0] < 305):
                                    theta = math.atan((475 - RedBall_lower[1])/(305 - RedBall_lower[0])) - math.radians(90)
                                else:
                                    theta = math.fabs(math.atan((475 - RedBall_lower[1])/(RedBall_lower[0] - 305))  - math.radians(90))
                                self.player.walk2(0.35, 0.0, 0.2*-theta)
                                time.sleep(0.1)
                        print "KICKING"

                        self.player.leftKick(1.0,1.1,2.3)
                        time.sleep(1.0)


                else:#free path
                    print "Free Path."
                    if (len(RedBall_lower)>1):
                        while(True):
                            RedBall_lower = self.player.getRedBall2()
                            print "In position Loop"
                            if(RedBall_lower[1] >=470 or RedBall_lower == [] or self.freePath(self.player.getPinkPlayers())):
                                self.player.killWalk()
                                break
                            if (RedBall_lower[0] == 305):
                                theta = 0.0
                            elif (RedBall_lower[0] < 305):
                                theta = math.atan((475 - RedBall_lower[1])/(305 - RedBall_lower[0])) - math.radians(90)
                            else:
                                theta = math.fabs(math.atan((475 - RedBall_lower[1])/(RedBall_lower[0] - 305))  - math.radians(90))
                            self.player.walk2(0.35, 0.0, 0.2*-theta)
                            time.sleep(0.1)

                        if (self.freePath(self.player.getPinkPlayers)):
                            print "No shot to kick"
                        else:
                            print "KICKING"

                            self.player.leftKick(1.0,1.1,2.3)
                            time.sleep(1.0)            
                    else: 
                        self.player.stop()
        elif (RedBall == [] and RedBall_lower == [] ):#ball not in view
            print "Trying to find ball."
            self.player.walk2(0.0, .75, .75)
        else:#locate ball
            print "Ball found, approaching."
            if (RedBall != []):
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

        time.sleep(.3)  


# self.player.walk(-theta*0.2)

# if (RedBall[0] == 320):
#     theta = 0.0
# elif (RedBall[0] < 320):
#     theta = math.atan((475 - RedBall[1])/(320 - RedBall[0])) - math.radians(90)
# else:
#     theta = math.fabs(math.atan((475 - RedBall[1])/(RedBall[0] - 320))  - math.radians(90))

# if (theta < -1.0):
#     theta = -1.0
# if (theta > 1.0):
#     theta = 1.0
# print "Theta: ", -theta*0.2

# self.player.walk(-theta*0.2)

