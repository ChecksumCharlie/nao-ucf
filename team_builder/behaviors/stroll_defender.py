from __future__ import division

import math
import time
from util import parameters as param

class LogicFor:
    def __init__(self, RobotGiven):
        self.player = RobotGiven

    def update(self):
        param.wrapFSM(self)


    def runFSM(self):    
        # get values
        RedBall = self.player.getRedBall()
        degrees_full_screen_sweep = 60 #approx.
        
        # begin behavior
        if (self.player.hasFallen()):
            self.player.initStance()
            
        self.player.RobotLegs.postureProxy.goToPosture( "StandInit", 0.5 )
                 
        # if ball not in sight, get ball in sight s.t. we face the general dir of the ball
        total_degrees_moved = 0
        while ( self.in_sight( RedBall ) == False and total_degrees_moved < 360):
            if ( self.vertical_RedBall_scan() ):
                break	
            self.rotate( math.radians( degrees_full_screen_sweep ) )
            total_degrees_moved += degrees_full_screen_sweep
            RedBall = self.player.getRedBall()
        
        if ( self.in_sight( RedBall ) == False):
            return
        
        # at this pt, robot sees the ball
        RedBall = self.player.getRedBall()
        
        self.goToBall( ) 
        
        #just walk around the ball for a while
        ctr = 0
        while ctr < 10 and (self.in_sight( RedBall ) or self.vertical_RedBall_scan()):
            self.walkAroundBall()
            ctr+=1
    
    # returns true red ball is above or below current field of vision
    # ~assumes head pitch stays at value where red ball was found
    # if red ball not found at all it returns to the original head pitch and returns false
    def vertical_RedBall_scan ( self ):
        names  = "HeadPitch"
        changes  = 0.5
        fractionMaxSpeed   = 1.0
        self.robot.RobotLegs.motion.changeAngles(names, changes, fractionMaxSpeed)
        RedBall = self.player.getRedBall()
        if( self.in_sight(RedBall) ):
            return True
        changes = -0.5
        self.robot.RobotLegs.motion.changeAngles(names, changes, fractionMaxSpeed)
    
    def in_sight( self, obj ):
        return obj != []    
    
    def goToBall(self):
        angles = self.player.getAngle("Head")
        print "Angles: ", angles
        RedBall = self.player.getRedBall()
        if (RedBall[1] > 450 and math.degrees(angles[0]) > 25):
            self.player.killWalk()
            self.player.setHeadAngle(0, "HeadPitch")
            self.player.walk(0.0)
            time.sleep(4)
        elif (RedBall[1] > 450):
            print "Adjusting sight."
            self.player.killWalk()
            print angles

            if (math.degrees(angles[0]) == 0):
                self.player.setHeadAngle(15, "HeadPitch")
            else:
                self.player.setHeadAngle(30, "HeadPitch")
        if (RedBall[0] == 320):
            theta = 0.0
        elif (RedBall[0] < 320):
            theta = math.atan((475 - RedBall[1]) / (320 - RedBall[0])) - math.radians(90)
        else:
            theta = math.fabs(math.atan((475 - RedBall[1]) / (RedBall[0] - 320)) - math.radians(90))

        if (theta < -1.0):
            theta = -1.0
        if (theta > 1.0):
            theta = 1.0
        print "Theta: ", -theta * 0.2
        while self.in_sight(RedBall) or self.vertical_RedBall_scan():
            self.player.walk(-theta * 0.2)
        self.player.killWalk()
    
    def walkAroundBall ( self ):
        ratio = 0.8
        self.robot.RobotLegs.motionProxy.moveTo(0.6*ratio,0.2*ratio,math.radians(360))
    
