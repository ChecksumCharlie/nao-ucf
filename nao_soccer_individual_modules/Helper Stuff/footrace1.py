### UNIVERSITY OF CENTRAL FLORIDA, COMPUTER SCIENCE ###
### written by Chris Cassian Olschewski ###
### under Dr. Heinrich and Dr. Suthankar ###

import sys
import time

from naoqi import ALProxy


def main(nao_ip, nao_port):
    
    # Init proxies.
    try:
        motionProxy = ALProxy("ALMotion",nao_ip, nao_port)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e

    try:
        postureProxy = ALProxy("ALRobotPosture", nao_ip, nao_port)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e
        
    try:
        redBallTracker = ALProxy("ALRedBallTracker", nao_ip, nao_port)
    except Exception, e:
        print "Could not create proxy to redBallTracker"
        print "Error was: ", e
        
    try:
        memoryProxy = ALProxy("ALMemory",nao_ip, nao_port)
    except Exception, e:
        print "Could not create proxy to ALMemory"
        print "Error was: ", e
        
    
    # First, set Head Stiffness to ON.
    motionProxy.setStiffnesses("Head", 1.0)
    
    # Then, start tracker.
    redBallTracker.startTracker()    
    
    # Will go to 1.0 then 0 radian
    # in two seconds
    motionProxy.post.angleInterpolation(
        ["HeadYaw"],
        [1.0, 0.0],
        [1  , 2],
        False
    )
    
    #RIGHT FOOT
    maxStepXRight = ["MaxStepX", 0.07]
    maxStepYRight = ["MaxStepY", 0.065]
    maxStepThetaRight = ["MaxStepTheta", 0.349]
    maxStepFrequencyRight = ["MaxStepFrequency", 1]
    stepHeightRight = ["StepHeight", 0.015]
    torsoWxRight = ["TorsoWx", 0.0] 
    torsoWyRight = ["TorsoWy", 0.0]
    
    #LEFT FOOT
    maxStepXLeft = ["MaxStepX", 0.7]
    maxStepYLeft = ["MaxStepY", 0.065]
    maxStepThetaLeft = ["MaxStepTheta", 0.349]
    maxStepFrequencyLeft = ["MaxStepFrequency", 1]
    stepHeightLeft = ["StepHeight", 0.015]
    torsoWxLeft = ["TorsoWx", 0.0] 
    torsoWyLeft = ["TorsoWy", 0.0]
    
    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    print "I'm ready, let's race" 

    crdArry = redBallTracker.getPosition()
    motionProxy.setWalkArmsEnabled(True, True)

    while True:
        # Get head position sensor value
        key = "Device/SubDeviceList/HeadYaw/Position/Sensor/Value"
        value = memoryProxy.getData(key)
        #print value
        # Check if move to left
        if value>=0.01:
            print "heading left"
            motionProxy.setWalkTargetVelocity(1.0,0.0,0.3,1.0,
                [#Left
                maxStepXRight,
                maxStepYRight,
                maxStepThetaRight,
                maxStepFrequencyRight,
                stepHeightRight,
                torsoWxRight,
                torsoWyRight],
                [#Right
                maxStepXLeft,
                maxStepYLeft,
                maxStepThetaLeft,
                maxStepFrequencyLeft,
                stepHeightLeft,
                torsoWxLeft,
                torsoWyLeft])
        # Check if move to right
        elif value<=-0.01:
            print "heading right"
            motionProxy.setWalkTargetVelocity(1.0,0.0,-0.3,1.0,
                [#Left
                maxStepXRight,
                maxStepYRight,
                maxStepThetaRight,
                maxStepFrequencyRight,
                stepHeightRight,
                torsoWxRight,
                torsoWyRight],
                [#Right
                maxStepXLeft,
                maxStepYLeft,
                maxStepThetaLeft,
                maxStepFrequencyLeft,
                stepHeightLeft,
                torsoWxLeft,
                torsoWyLeft])
        # Check if need to stop
        else:
            print "heading straight"
            motionProxy.setWalkTargetVelocity(1.0,0.0,0.0,1.0,
                [#Left
                maxStepXRight,
                maxStepYRight,
                maxStepThetaRight,
                maxStepFrequencyRight,
                stepHeightRight,
                torsoWxRight,
                torsoWyRight],
                [#Right
                maxStepXLeft,
                maxStepYLeft,
                maxStepThetaLeft,
                maxStepFrequencyLeft,
                stepHeightLeft,
                torsoWxLeft,
                torsoWyLeft])
        
        time.sleep(.5)
        crdArry = redBallTracker.getPosition()
        if (crdArry[0]>=.3 and crdArry[0]!=0):
            print crdArry[0]
            break
    
    motionProxy.setWalkTargetVelocity(0.0,0.0,0.0,0.0)
    # Stop tracker and remove head stiffness.
    redBallTracker.stopTracker()
    motionProxy.setStiffnesses("Head", 0.0)
    
        
if __name__ == "__main__":

    nao_ip = "127.0.0.1"
    nao_port = 9560

    if len(sys.argv) <= 2:
        print "Usage THISFILE.py robotIP robotPORT(optional default: 127.0.0.1 9559)"
    else:
        nao_ip = sys.argv[1]
        nao_port = sys.argv[2]

    main(nao_ip, nao_port)
            
            