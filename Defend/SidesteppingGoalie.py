### UNIVERSITY OF CENTRAL FLORIDA, COMPUTER SCIENCE ###
### written by Chris Cassian Olschewski ###
### under Dr. Heinrich and Dr. Suthankar ###

import sys
import time

from naoqi import ALProxy


def main(IP, PORT):
    
    # Init proxies.
    try:
        motionProxy = ALProxy("ALMotion",IP, PORT)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e

    try:
        postureProxy = ALProxy("ALRobotPosture", IP, PORT)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e
        
    try:
        ballTrackerProxy = ALProxy("ALRedBallTracker", IP, PORT)
    except Exception, e:
        print "Could not create proxy to ballTrackerProxy"
        print "Error was: ", e
        
    try:
        memoryProxy = ALProxy("ALMemory",IP, PORT)
    except Exception, e:
        print "Could not create proxy to ALMemory"
        print "Error was: ", e
        
    
    # First, set Head Stiffness to ON.
    motionProxy.setStiffnesses("Head", 1.0)
    
    # Then, start tracker.
    ballTrackerProxy.startTracker()
    
    # Will go to 1.0 then 0 radian
    # in two seconds
    motionProxy.post.angleInterpolation(
        ["HeadYaw"],
        [1.0, 0.0],
        [1 , 2],
        False
    )
    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)
    print "I'm ready, defending UCF's goal"

    while True:
        # Get head position sensor value
        key = "Device/SubDeviceList/HeadYaw/Position/Sensor/Value"
        value = memoryProxy.getData(key)
        print value
        # Check if move to left
        if value>=0.1:
            motionProxy.setWalkTargetVelocity(0.0, 1.0, 0.0, 1.0)
        # Check if move to right
        elif value<=-0.1:
            motionProxy.setWalkTargetVelocity(0.0, -1.0, 0.0, 1.0)
        # Check if need to stop
        else:
            motionProxy.setWalkTargetVelocity(0.0, 0.0, 0.0, 0.0)
        
        time.sleep(1)
    
    # Stop tracker and remove head stiffness.
    ballTrackerProxy.stopTracker()
    motionProxy.setStiffnesses("Head", 0.0)
    
        
if __name__ == "__main__":

    IP = "127.0.0.1"
    PORT = 9559

    if len(sys.argv) <= 2:
        print "Usage THISFILE.py robotIP robotPORT(optional default: 127.0.0.1 9559)"
    else:
        IP = sys.argv[1]
        PORT = sys.argv[2]

    main(IP, PORT)