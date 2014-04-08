'''
Created on Apr 2, 2014

@author: Sarah
'''

import time
from naoqi import ALProxy

class Robot ( object ):
    
    def __init__(self, IP, PORT):
        
        self.isInitialized = False
        
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
        
    
    def Initialize (self, behavior):
        
        self.behavior = behavior
        # First, set Head Stiffness to ON.
        self.motionProxy.setStiffnesses("Head", 1.0)
        self.motionProxy.setStiffnesses("Body", 1.0)
        self.motionProxy.setWalkArmsEnabled(True, True)
        # Will go to 1.0 then 0 radians in two seconds
        self.motionProxy.post.angleInterpolation ( ["HeadYaw"], [1.0, 0.0], [1, 2], False )
        
        # Then, start tracker.
        self.ballTrackerProxy.startTracker()    
        time.sleep(.01)
        # Send NAO to Pose Init
        self.postureProxy.goToPosture("StandInit", 0.5)
        #redBallPos = self.ballTrackerProxy.getPosition()
        
        self.isInitialized = True
    
    def Run (self):
        if(self.isInitialized == False):
            print "Must call Initialize(behavior) first!"
            return
        self.behavior.Run(self)
        
    
    def Dispose (self):
        
        self.motionProxy.setWalkTargetVelocity ( 0.0, 0.0, 0.0, 0.0 )
        # Stop tracker and remove head stiffness.
        self.ballTrackerProxy.stopTracker ()
        self.postureProxy.goToPosture ( "StandInit", 0.5 )
        self.motionProxy.setStiffnesses ( "Head", 0.0 )
        self.motionProxy.setStiffnesses("Body", 0.0)
        
        if ( self.memoryProxy.isRunning(0) ):
            self.memoryProxy.stop(None)
            
        if ( self.memoryProxy.isRunning(0) ):    
            self.postureProxy.stop(None)
            
        if ( self.memoryProxy.isRunning(0) ):
            self.motion.stop(None)
            
        if ( self.memoryProxy.isRunning(0) ):
            self.ballTrackerProxy.stop(None)
            
        self.isInitialized = False