'''
Created on Apr 1, 2014

@author: Sarah
'''
import math 
import time
from naoqi import ALProxy

class Robot (object):
    
    def __init__(self, IP, PORT):
        self.motionProxy = ALProxy("ALMotion", IP, PORT)
        self.memoryProxy = ALProxy("ALMemory", IP, PORT)
        self.postureProxy = ALProxy("ALRobotPosture", IP, PORT)
        self.ballTrackerProxy = ALProxy("ALRedBallTracker", IP, PORT)
                
        # Defaults for feet data
        #RIGHT FOOT
        self.maxStepXRight = ["MaxStepX", 0.07]
        self.maxStepYRight = ["MaxStepY", 0.065]
        self.maxStepThetaRight = ["MaxStepTheta", 0.349]
        self.maxStepFrequencyRight = ["MaxStepFrequency", 1]
        self.stepHeightRight = ["StepHeight", 0.015]
        self.torsoWxRight = ["TorsoWx", 0.0] 
        self.torsoWyRight = ["TorsoWy", 0.0]
        
        #LEFT FOOT
        self.maxStepXLeft = ["MaxStepX", 0.7]
        self.maxStepYLeft = ["MaxStepY", 0.065]
        self.maxStepThetaLeft = ["MaxStepTheta", 0.349]
        self.maxStepFrequencyLeft = ["MaxStepFrequency", 1]
        self.stepHeightLeft = ["StepHeight", 0.015]
        self.torsoWxLeft = ["TorsoWx", 0.0] 
        self.torsoWyLeft = ["TorsoWy", 0.0]
        
    
    def Initialize (self):
        # First, set Head Stiffness to ON.
        self.motionProxy.setStiffnesses("Head", 1.0)
        self.motionProxy.setWalkArmsEnabled(True, True)
        # Will go to 1.0 then 0 radians in two seconds
        self.motionProxy.post.angleInterpolation ( ["HeadYaw"], [1.0, 0.0], [1, 2], False )
        
        # Then, start tracker.
        self.ballTrackerProxy.startTracker()    
        
        # Send NAO to Pose Init
        self.postureProxy.goToPosture("StandInit", 0.5)
      
        #redBallPos = self.ballTrackerProxy.getPosition()
    
    def Run (self):
        
        key = "Device/SubDeviceList/HeadYaw/Position/Sensor/Value"
        
        while ( True ):
            # Get head position sensor value
            value = self.memoryProxy.getData (key)
            self.memoryProxy.setData (key)
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
            
            ballPos = self.ballTrackerProxy.getPosition ()
            if ( math.sqrt( math.pow( ballPos[0], 2 ) + math.pow( ballPos[1],2 ) ) <= 0.3 and ballPos[0] != 0 ):
            #    print ( "Distance from Ball: ", math.sqrt( math.pow( ballPos[0], 2 ) + math.pow( ballPos[1], 2 ) ) )
                break
            time.sleep(.5)
    
    def Dispose (self):
        self.motionProxy.setWalkTargetVelocity ( 0.0, 0.0, 0.0, 0.0 )
        # Stop tracker and remove head stiffness.
        self.ballTrackerProxy.stopTracker ()
        self.postureProxy.goToPosture ( "StandInit", 0.5 )
        self.motionProxy.setStiffnesses ( "Head", 0.0 )
        
        if ( self.memoryProxy.isRunning(0) ):
            self.memoryProxy.stop(None)
        if ( self.memoryProxy.isRunning(0) ):    
            self.postureProxy.stop(None)
        if ( self.memoryProxy.isRunning(0) ):
            self.motion.stop(None)
        if ( self.memoryProxy.isRunning(0) ):
            self.ballTrackerProxy.stop(None)

if __name__ == '__main__':    
    IP = "127.0.0.1"
    PORT = 9560
    Beckham = Robot ( IP, PORT )
    Beckham.Initialize ()
    print "Im Alive"
    Beckham.Run()
    Beckham.Dispose()
    