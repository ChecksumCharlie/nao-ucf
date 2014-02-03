from naoqi import ALProxy
import time

IP = "127.0.0.1"
PORT = 9559

motion = ALProxy("ALMotion", IP, PORT)
redBallTracker = ALProxy("ALRedBallTracker", IP, PORT)

motion.setStiffnesses("Body", 1.0)

redBallTracker.startTracker()
time.sleep(.01)
       
if redBallTracker.isActive():
    crdArry = redBallTracker.getPosition()
    print "within if-else"
    print crdArry[0]
    print crdArry[1]
    while crdArry[0] >= 0.4:
        print "Still active:TRACKING SUCCESFUL"
        motion.moveTo(crdArry[0],crdArry[1],0)
        time.sleep(.01)
        crdArry = redBallTracker.getPosition()
        print crdArry[0]
        print crdArry[1]
else:
    print "Failed Detection"
           
redBallTracker.stopTracker()

motion.setStiffnesses("Body", 0.0)

print "MODULE STOPPED."
