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
        self.goToBall() 
        
        # find goal
        bufferDist = 0.2
        Goal = self.player.getYellowGoal()   # opponent's goal
        while ( self.in_sight( Goal ) == False ):
            if ( self.vertical_Goal_scan() ):
                Goal = self.player.getYellowGoal()
                RedBall = self.player.getRedBall()
                ctr = 0
                while ( self.in_sight( RedBall ) == False and self.in_sight( Goal ) == False and ctr < 3):
                    # walk backwards
                    num_steps = 2
                    step_length = 0.07
                    dist = num_steps * step_length
                    self.robot.RobotLegs.motionProxy.moveTo(-1*dist,0.0,0.0)
                    RedBall = self.player.getRedBall()
                    Goal = self.player.getYellowGoal()
                    ctr+=1
                if ctr >= 3:
                    return # to look for ball again
            else:
                self.walkSquareAroundBall( bufferDist , 0)
                Goal = self.player.getYellowGoal()
        
        # at this pt, robot sees ball and goal
        RedBall = self.player.getRedBall()
        Goal = self.player.getYellowGoal()
        # just aims towards found goal location which is center point of found goal
        self.aim( Goal )
        
        self.goToBall()
        
        # current attempt just tries to walk ball into goal
        self.robot.RobotLegs.motionProxy.moveTo(1.4*15,0,0)
    
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
    
    # looks up for goal... returns true if goal is found
    def vertical_Goal_scan ( self ):
        print 'vertical Goal scan... should not ever happen'
        names  = "HeadPitch"
        changes  = 0.5
        fractionMaxSpeed   = 1.0
        self.robot.RobotLegs.motion.changeAngles(names, changes, fractionMaxSpeed)
        RedBall = self.player.getRedBall()
        if( self.in_sight(RedBall) ):
            return True
        changes = -0.5
        self.robot.RobotLegs.motion.changeAngles(names, changes, fractionMaxSpeed)
    
    # walks around the ball in a square until ball and goal are both in sight (ie in the same horizontal range)
    def walkSquareAroundBall ( self, bufferDist, count ):
        if count > 9:
            return
        radius = 0.06
        moveDist = radius + bufferDist
        rotate = False
        #side step
        self.robot.RobotLegs.motionProxy.moveTo(0.0,moveDist,0)
        RedBall = self.player.getRedBall()
        if ( not self.in_sight( RedBall ) ):
            rotate = True
        if rotate:
            self.robot.RobotLegs.motionProxy.moveTo(0.0,0.0,math.radians(45))
        RedBall = self.player.getRedBall()
        Goal = self.player.getYellowGoal()
        if ( self.in_sight( RedBall )  and  self.in_sight( Goal ) ):
            return
        if rotate:
            self.robot.RobotLegs.motionProxy.moveTo(0.0,0.0,math.radians(45))
        self.walkSquareAroundBall( bufferDist, count+1 )
    
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
    
    def in_camera_center( self, Goal ):
        if not self.in_sight( Goal ):
            self.vertical_Goal_scan()
        Goal = self.player.getYellowGoal()
        if not self.in_sight( Goal ):
            return False
        return Goal[0] < 260 and Goal[0] > 140
    
    # AIM: walk around ball until the ball is relatively between goal posts
    def aim (self, Goal):
        while ( self.vertical_RedBall_scan() and not self.in_camera_center( Goal ) ):
            self.walkAroundBall()
            Goal = self.player.getYellowGoal()
    
