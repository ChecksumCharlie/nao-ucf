### UNIVERSITY OF CENTRAL FLORIDA, COMPUTER SCIENCE ###
### written by Chris Cassian Olschewski ###
### under Dr. Heinrich and Dr. Suthankar ###

import sys
import time

from naoqi import ALProxy


def start(nao_ip, nao_port):
    
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
    
   
    
    # Will go to 1.0 then 0 radian
    # in two seconds
    motionProxy.post.angleInterpolation(
        ["HeadYaw"],
        [1.0, 0.0],
        [1 , 2],
        False
    )
    # Postures available: Crouch, LyingBack, LyingBelly, Sit, SitRelax, Stand, StandInit, StandZero
    postureProxy.goToPosture("StandInit", 0.5)
    print "I'm ready, defending UCF's goal"

    
    
        
if __name__ == "__main__":

    nao_ip = "127.0.0.1"
    nao_port = 9559

    if len(sys.argv) <= 2:
        print "Usage THISFILE.py robotIP robotPORT(optional default: 127.0.0.1 9559)"
    else:
        nao_ip = sys.argv[1]
        nao_port = sys.argv[2]
    start(nao_ip, nao_port)
