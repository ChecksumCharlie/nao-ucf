from naoqi import ALProxy
import time
import sys
import math

def StiffnessOn(proxy):
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
    
def main():
    robotIP = "127.0.0.1"
    Port = 9560
    try:
        motionProxy = ALProxy("ALMotion", robotIP, Port)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e
        
    redBallTracker = ALProxy("ALRedBallTracker", robotIP, Port)
    
    StiffnessOn(motionProxy)
    
    redBallTracker.startTracker()
    while (not redBallTracker.isNewData()):
        print "aquiring tracker"
        time.sleep(.1)
    
    #Track Ball and move to it
    if redBallTracker.isActive():
        crdArry = redBallTracker.getPosition()
        print "within if-else"
        print crdArry[0]
        print crdArry[1]
        
        while crdArry[0] >= 0.3:
            print "Still active:TRACKING SUCCESFUL"
            crdArry = redBallTracker.getPosition()
            print crdArry[0]
            print crdArry[1]
            motionProxy.setWalkTargetVelocity(1.0, 0.0, 0.0, 1.0)
    else:
        print "Failed Detection"
        
    print "DERP"    
    
    motionProxy.setWalkTargetVelocity(0.0, 0.0, 0.0, 0.0)
    
    motionProxy.moveTo(.7, 0.0, -2.0)
    time.sleep(.1)
    
    motionProxy.setWalkTargetVelocity(.8, 0.0, 0.0, 1.0)
    time.sleep(4)
    
    motionProxy.setWalkTargetVelocity(0.0, 0.0, 0.0, 0.0)
    
#     theta = 0.0 
#     while theta <= 35: 
#        crdArry = redBallTracker.getPosition()
#        print (crdArry[0])
#        print (crdArry[1])
#        theta = math.degrees(math.atan(math.fabs(crdArry[1])/math.fabs(crdArry[0])))
#        time.sleep(.01)
#        print "X theta: ", theta
#        motionProxy.setWalkTargetVelocity(0.0, 1.0, 0.0, 1.0)
#        
#    motionProxy.setWalkTargetVelocity(0.0, 0.0, 0.0, 0.0)
#    
#    while theta <=45:
#         crdArry = redBallTracker.getPosition()
#         print (crdArry[0])
#         print (crdArry[1])
#         theta = math.degrees(math.atan(math.fabs(crdArry[1])/math.fabs(crdArry[0])))
#         time.sleep(.01)
#         print "theta: ", theta
#         motionProxy.setWalkTargetVelocity(1.0, 0.0, 0.0, 1.0)
#     
#     motionProxy.setWalkTargetVelocity(0.0, 0.0, 0.0, 0.0)
#     
#     time.sleep(1)
#        
#     motionProxy.move(1.0,-1.0,0.0,1.0)

if __name__ == "__main__":
    robotIp = "127.0.0.1"

    if len(sys.argv) <= 1:
        print "Usage python motion_walk.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main()