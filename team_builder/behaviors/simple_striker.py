from __future__ import division

import math
import time


class LogicFor:
    def __init__(self, RobotGiven):
        self.player = RobotGiven

    def update(self):
            self.player.RobotLegs.postureProxy.goToPosture("StandInit", 0.5)
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
                print "No enemy, goal and ball in sight."
                
                if (RedBall [1] > 400):
                    
                    self.player.killWalk()
                    print "Ball soon leavin vision... correcting."
                    angles = self.player.getAngle("Head")
                    print angles
                    if (math.degrees(angles[1]) >= 14.0):
                        self.player.tiltHead(math.radians(30))
                    else:
                        self.player.tiltHead(math.radians(15))

                    if (math.degrees(angles[1]) >= 29):
                        print "Positioning time."
                        if (len(Goal) == 4):
                            self.player.tiltHead(math.radians(0))
                            self.player.walk(0)
                            time.sleep(8)
                            
                else:
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
            elif (RedBall != [] and Enemy != [] and Goal == []):
                print "Time to defend, no goal in sight."
            elif (RedBall == [] and Enemy != [] and Goal != []):
                print "Cannot find ball, enemy and goal in sight. Relocating."
            else:
                self.player.killWalk()
                print "Other case."
