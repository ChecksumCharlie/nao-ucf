from naoqi import ALProxy
import time

#def Chase():
IP = "127.0.0.1"
PORT = 9560

motion = ALProxy("ALMotion", IP, PORT)
ballTrackerProxy = ALProxy("ALRedBallTracker", IP, PORT)

motion.setStiffnesses("Body", 1.0)

ballTrackerProxy.startTracker()
time.sleep(.01)
       
motion.setWalkArmsEnabled(True, True)

while (not ballTrackerProxy.isNewData()):
        print "aquiring tracker"
        time.sleep(.1)

if ballTrackerProxy.isActive():
    crdArry = ballTrackerProxy.getPosition()
    print "within if-else"
    print crdArry[0]
    print crdArry[1]
    while crdArry[0] >= 0.4:
        print "Still active:TRACKING SUCCESFUL"
        motion.setWalkTargetVelocity(.8,0.0,0.0,1.0,
                [ # LEFT FOOT
                ["MaxStepX", 0.065],
                ["StepHeight", 0.01],
                ["TorsoWx", 0.0],
                ["TorsoWy", 0.0], 
                ["MaxStepTheta", .001]],
                [ # RIGHT FOOT
                ["StepHeight", 0.01],
                ["MaxStepX", 0.065],
                ["TorsoWx", 0.0], 
                ["TorsoWy", 0.0],
                ["MaxStepTheta", .001]] )
        time.sleep(.01)
        crdArry = ballTrackerProxy.getPosition()
        print crdArry[0]
        print crdArry[1]
else:
    print "Failed Detection"
           
ballTrackerProxy.stopTracker()

motion.setStiffnesses("Body", 0.0)

print "MODULE STOPPED."
