#Chris Cassian Olschewski
#Definding player module

# import sys
import time
from naoqi import ALProxy

IP = "127.0.0.1"
PORT = 9560

motion = ALProxy("ALMotion", IP, 9559)
motion.setStiffnesses("Body", 1.0)
motion.moveInit()


while True:
    
    id = motion.post.moveTo(0.5, 0, 0)
    motion.wait(id, 0)


# print "Connecting to", IP, "with port", PORT
# motion = ALProxy("ALMotion", IP, PORT)
# redBallTracker = ALProxy("ALRedBallTracker", IP, PORT)
# 
# # First, set Head Stiffness to ON.
# motion.setStiffnesses("Head", 1.0)
# motion.setStiffnesses("Body", 1.0)
# 
# # Then, start tracker.
# redBallTracker.startTracker()
# 
# print "ALRedBallTracker successfully started, now show your face to Nao!"
# print "ALRedBallTracker will be stopped in 3 s."
# 
# time.sleep(3)
# 
# 
# if redBallTracker.isActive() == True:
#     print "Still active TRACKING SUCCESFUL"
#     crdArry = redBallTracker.getPosition()
#     print crdArry[0]
#     print crdArry[1]
#     print crdArry[2]
#     motion.moveTo(crdArry[0],crdArry[1],crdArry[2])
# else:
#     print "Failed Detection"
# 
# 
# redBallTracker.stopTracker()
# motion.setStiffnesses("Head", 0.0)
# 
# print "ALRedBallTracker stopped."