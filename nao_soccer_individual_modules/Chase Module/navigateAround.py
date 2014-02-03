from naoqi import ALProxy
import time

IP = "127.0.0.1"
PORT = 9559

def StiffnessOn(proxy):
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
    
def main(Port):
    robotIP = "127.0.0.1"
    try:
        motionProxy = ALProxy("ALMotion", robotIP, Port)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e
        
    redBallTracker = ALProxy("ALRedBallTracker", robotIP, Port)
    
    StiffnessOn(motionProxy)
    
    if redBallTracker.isActive():
        crdArry = redBallTracker.getPosition()
    else:
        print "Failed Detection"
    
    