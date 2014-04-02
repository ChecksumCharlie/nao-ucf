#Kristjan Arumae
#11/4/13
#Simple Motion + TRACKING

import sys
import time
from naoqi import ALProxy

IP = "127.0.0.1"
PORT = 9560

print "Connecting to", IP, "with port", PORT
motion = ALProxy("ALMotion", IP, PORT)
ballTrackerProxy = ALProxy("ALRedBallTracker", IP, PORT)

# First, set Head Stiffness to ON.
motion.setStiffnesses("Head", 1.0)
motion.setStiffnesses("Body", 1.0)

# Then, start tracker.
ballTrackerProxy.startTracker()

print "ALRedBallTracker successfully started, now show your face to Nao!"
print "ALRedBallTracker will be stopped in 3 s."

time.sleep(3)


if ballTrackerProxy.isActive() == True:
    print "Still active TRACKING SUCCESFUL"
    crdArry = ballTrackerProxy.getPosition()
    print crdArry[0]
    print crdArry[1]
    print crdArry[2]
    motion.moveTo(crdArry[0],crdArry[1],crdArry[2])
else:
    print "Failed Detection"


ballTrackerProxy.stopTracker()
motion.setStiffnesses("Head", 0.0)

print "ALRedBallTracker stopped."