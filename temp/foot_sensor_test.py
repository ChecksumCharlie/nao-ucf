
import sys
import time
from naoqi import ALProxy

# Robot ip address and port
IP = "127.0.0.1"
PORT = 9560


motion = ALProxy("ALMotion", IP, PORT)
memory = ALProxy("ALMemory",IP, PORT)
posture = ALProxy("ALRobotPosture",IP,PORT)

motion.setStiffnesses("Body", 1.0)

# posture.post.goToPosture("StandInit", 0.5)

while (True):

	key = "Device/SubDeviceList/LFoot/FSR/FrontLeft/Sensor/Value"
	value = memory.getData(key)
	print "Left Foot -> FrontLeft: " + str(value)

	key = "Device/SubDeviceList/LFoot/FSR/FrontRight/Sensor/Value"
	value = memory.getData(key)
	print "Left Foot -> FrontRight: " + str(value)

	key = "Device/SubDeviceList/LFoot/FSR/RearLeft/Sensor/Value"
	value = memory.getData(key)
	print "Left Foot -> RearLeft: " + str(value)

	key = "Device/SubDeviceList/LFoot/FSR/RearRight/Sensor/Value"
	value = memory.getData(key)
	print "Left Foot -> RearRight: " + str(value)


	key = "Device/SubDeviceList/RFoot/FSR/FrontLeft/Sensor/Value"
	value = memory.getData(key)
	print "Right Foot -> FrontLeft: " + str(value)

	key = "Device/SubDeviceList/RFoot/FSR/FrontRight/Sensor/Value"
	value = memory.getData(key)
	print "Right Foot -> FrontRight: " + str(value)

	key = "Device/SubDeviceList/RFoot/FSR/RearLeft/Sensor/Value"
	value = memory.getData(key)
	print "Right Foot -> RearLeft: " + str(value)

	key = "Device/SubDeviceList/RFoot/FSR/RearRight/Sensor/Value"
	value = memory.getData(key)
	print "Right Foot -> RearRight: " + str(value)

	print ""

	
	motion.post.moveTo(3, 0, 0)
	time.sleep(1)
           
# Safe Exit for Webots' sake
sys.exit(0)
