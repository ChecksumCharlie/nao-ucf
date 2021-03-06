#Chris Cassian Olschewski
#Defending player module

import sys
import motion
import time
from naoqi import ALProxy


def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)


def main(robotIP):
    # Init proxies.
    try:
        motionProxy = ALProxy("ALMotion", robotIP, 9559)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e
        
    try:
        redBallTracker = ALProxy("ALRedBallTracker", robotIP, 9559)
    except Exception, e:
        print "Could not create proxy to redBallTracker"
        print "Error was: ", e

    # Set NAO in Stiffness On
    StiffnessOn(motionProxy)

    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    #####################
    ## Enable arms control by Walk algorithm
    #####################
    motionProxy.setWalkArmsEnabled(True, True)
    #~ motionProxy.setWalkArmsEnabled(False, False)

    #####################
    ## FOOT CONTACT PROTECTION
    #####################
    #~ motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", False]])
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

    redBallTracker.startTracker()
    
    time.sleep(4.0)

    while True:
        
        #TARGET VELOCITY: MOVE RIGHT
        
        #if (crdArry[1] < 0.0):
        X = 0.0
        Y = -1.0
        Theta = 0.0
        Frequency =1.0
        motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    
        time.sleep(4.0)
        
        X = 0.0
        Y = -0.5
        Theta = 0.0
        Frequency =1.0
        motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
        
        time.sleep(2.0)
        
        #TARGET VELOCITY: MOVE RIGHT
        #if (crdArry[1] >= 0.0):
        X = 0.0
        Y = 1.0
        Theta = 0.0
        Frequency =1.0
        motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    
        time.sleep(4.0)
    
    

    #TARGET VELOCITY: STOP
    X = 0.0
    Y = 0.0
    Theta = 0.0
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

    redBallTracker.stopTracker()

if __name__ == "__main__":
    nao_ip = "127.0.0.1"
    nao_port = 9559

    if len(sys.argv) <= 2:
        print "Usage THISFILE.py robotIP robotPORT(optional default: 127.0.0.1 9559)"
    else:
        nao_ip = sys.argv[1]
        nao_port = sys.argv[2]

    main(nao_ip)