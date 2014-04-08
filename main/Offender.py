'''
Created on Apr 4, 2014

@author: Sarah
'''

import math
import time
from Behavior import Behavior

class Offender ( Behavior ):

    def __init__ ( self ):
        Behavior.__init__ ( self )
    
    def Run ( self, robot ):
        Behavior.Run(self, robot)
        ballPos = self.chase_ball ( robot )
        if ( math.sqrt( math.pow( ballPos[0], 2 ) + math.pow( ballPos[1],2 ) ) <= 0.3 and ballPos[0] != 0 ):
            self.position ( robot )
            self.aim ( robot )
            self.kick ( robot )
        return
    
    def chase_ball ( self, robot ):
        key = "Device/SubDeviceList/HeadYaw/Position/Sensor/Value"
        while True:
            # Get head position sensor value
            value = self.memoryProxy.getData ( key )
            #print value
            # Check if move to left
            if ( value >= 0.01 ):
                print "heading left"
                #motionProxy.stopMove()
                self.motionProxy.setWalkTargetVelocity ( 1.0, 0.0, value, 1.0,
                    [#Left
                    self.maxStepXRight,
                    #maxStepYRight,
                    self.maxStepThetaRight,
                    self.maxStepFrequencyRight,
                    self.stepHeightRight,
                    self.torsoWxRight,
                    self.torsoWyRight],
                    [#Right
                    self.maxStepXLeft,
                    #maxStepYLeft,
                    self.maxStepThetaLeft,
                    self.maxStepFrequencyLeft,
                    self.stepHeightLeft,
                    self.torsoWxLeft,
                    self.torsoWyLeft])
            # Check if move to right
            elif ( value <= -0.01 ):
                print "heading right"
                #motionProxy.stopMove()
                self.motionProxy.setWalkTargetVelocity ( 1.0, 0.0, value, 1.0,
                    [#Left
                    self.maxStepXRight,
                    #maxStepYRight,
                    self.maxStepThetaRight,
                    self.maxStepFrequencyRight,
                    self.stepHeightRight,
                    self.torsoWxRight,
                    self.torsoWyRight],
                    [#Right
                    self.maxStepXLeft,
                    #maxStepYLeft,
                    self.maxStepThetaLeft,
                    self.maxStepFrequencyLeft,
                    self.stepHeightLeft,
                    self.torsoWxLeft,
                    self.torsoWyLeft])
            # Check if need to stop
            else:
                print "heading straight"
                self.motionProxy.setWalkTargetVelocity ( 1.0, 0.0, 0.0, 1.0,
                    [#Left
                    self.maxStepXRight,
                    #maxStepYRight,
                    #["MaxStepTheta", 0.0],
                    self.maxStepFrequencyRight,
                    self.stepHeightRight,
                    self.torsoWxRight,
                    self.torsoWyRight],
                    [#Right
                    self.maxStepXLeft,
                    #maxStepYLeft,
                    #["MaxStepTheta", 0.0],
                    self.maxStepFrequencyLeft,
                    self.stepHeightLeft,
                    self.torsoWxLeft,
                    self.torsoWyLeft])
            
            time.sleep (.5)
            
            ballPos = self.ballTrackerProxy.getPosition ()
            if ( math.sqrt( math.pow( ballPos[0], 2 ) + math.pow( ballPos[1],2 ) ) <= 0.3 and ballPos[0] != 0 ):
                print ( "Distance from Ball: ", math.sqrt( math.pow( ballPos[0], 2 ) + math.pow( ballPos[1], 2 ) ) )
                break
        return ballPos
        #chase ball here
    
    def position ( self, robot ):
        return
        #position module
        
    def aim ( self, robot ):
        return
        #does not exists currently
    
    def kick ( self, robot ):
        return
        #kick module
    
    #returns the [x,y] of the desired location for the calculated spot for kicking
def get_target_loc(ball_loc, goal_loc, dist):
    target_loc = ball_loc
    if ball_loc[1]==0:
        target_loc[0] -= dist
    else:
        L1 = goal_loc[0]-ball_loc[0]
        L2 = goal_loc[1]-ball_loc[1]
        L3 = distance(L1,L2)
        x = dist*L1/L3
        y = dist*L2/L3
        target_loc[0]-=x
        target_loc[1]-=y
    return target_loc
    
# returns the distance between points a and b
def distance(a, b):
    return math.sqrt(math.pow(a,2)+math.pow(b,2))

# prints string str followed by the coordinates [x,y] of loc
def print_coordinates(str,loc):
    str = str,loc[0],loc[1]
    print str 
    