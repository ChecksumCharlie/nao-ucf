from naoqi import ALProxy
import time
import sys
import math
import almath

def StiffnessOn(proxy):
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 0.1 
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
    
def main():
    robotIP = "127.0.0.1"
    Port = 9560
    
    chase(robotIP, Port, 0.3)
    
    try:
        motionProxy = ALProxy("ALMotion", robotIP, Port)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e
        
    try:
        redBallTracker = ALProxy("ALRedBallTracker", robotIP, Port)
    except Exception, e:
        print "Could not create proxy to redBallTracker"
        print "Error was: ", e
   
    maxStepXRight = ["MaxStepX", 0.07]
    maxStepFrequencyRight = ["MaxStepFrequency", 1]
    stepHeightRight = ["StepHeight", 0.015]
    torsoWxRight = ["TorsoWx", 0.0] 
    torsoWyRight = ["TorsoWy", 0.0]
    
    #LEFT FOOT
    maxStepXLeft = ["MaxStepX", 0.7]
    maxStepFrequencyLeft = ["MaxStepFrequency", 1]
    stepHeightLeft = ["StepHeight", 0.015]
    torsoWxLeft = ["TorsoWx", 0.0] 
    torsoWyLeft = ["TorsoWy", 0.0]    
    
    motionProxy.setWalkTargetVelocity(0.0, 0.0, 0.0, 0.0)
    
    motionProxy.moveTo(1.0, 0.0, -2.5)
    
    motionProxy.setWalkTargetVelocity(1.0,0.0,0,1.0,
                [#Left
                maxStepXRight,
                #maxStepYRight,
                ["MaxStepTheta", 0.349],
                maxStepFrequencyRight,
                stepHeightRight,
                torsoWxRight,
                torsoWyRight],
                [#Right
                maxStepXLeft,
                #maxStepYLeft,
                ["MaxStepTheta", 0.349],
                maxStepFrequencyLeft,
                stepHeightLeft,
                torsoWxLeft,
                torsoWyLeft])
    
    time.sleep(1)
    
    chase(robotIP, Port, 0.3)
    
    motionProxy.setWalkTargetVelocity(0.0, 0.0, 0.0, 0.0)

def chase(nao_ip, nao_port, threshold):
    
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
        print value
        # Check if move to left
        if value>=0.01:
            print "heading left"
            #motionProxy.stopMove()
            motionProxy.setWalkTargetVelocity(1.0,0.0,value,1.0,
                [#Left
                maxStepXRight,
                #maxStepYRight,
                ["MaxStepTheta", 0.349],
                maxStepFrequencyRight,
                stepHeightRight,
                torsoWxRight,
                torsoWyRight],
                [#Right
                maxStepXLeft,
                #maxStepYLeft,
                ["MaxStepTheta", 0.349],
                maxStepFrequencyLeft,
                stepHeightLeft,
                torsoWxLeft,
                torsoWyLeft])
        # Check if move to right
        elif value<=-0.01:
            print "heading right"
            #motionProxy.stopMove()
            motionProxy.setWalkTargetVelocity(1.0,0.0,value,1.0,
                [#Left
                maxStepXRight,
                #maxStepYRight,
                ["MaxStepTheta", 0.349],
                maxStepFrequencyRight,
                stepHeightRight,
                torsoWxRight,
                torsoWyRight],
                [#Right
                maxStepXLeft,
                #maxStepYLeft,
                ["MaxStepTheta", 0.349],
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
                #maxStepYRight,
                #["MaxStepTheta", 0.0],
                maxStepFrequencyRight,
                stepHeightRight,
                torsoWxRight,
                torsoWyRight],
                [#Right
                maxStepXLeft,
                #maxStepYLeft,
                #["MaxStepTheta", 0.0],
                maxStepFrequencyLeft,
                stepHeightLeft,
                torsoWxLeft,
                torsoWyLeft])
        
        time.sleep(.5)
        crdArry = redBallTracker.getPosition()
        if (math.sqrt(math.pow(crdArry[0], 2) +math.pow(crdArry[1],2))<=threshold and crdArry[0]!=0):
            print "distance from Ball: ",math.sqrt(math.pow(crdArry[0], 2) +math.pow(crdArry[1],2))
            break
    
    motionProxy.setWalkTargetVelocity(0.0,0.0,0.0,0.0)
    # Stop tracker and remove head stiffness.
    redBallTracker.stopTracker()
    motionProxy.setStiffnesses("Head", 0.0)
    return


if __name__ == "__main__":
    robotIp = "127.0.0.1"

    if len(sys.argv) <= 1:
        print "Usage python motion_walk.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main()