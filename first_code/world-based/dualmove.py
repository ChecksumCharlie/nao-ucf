# Program 3: moving two robots at the same time

import sys
import time
from naoqi import ALProxy
#import seeker

# Robot ip addresses and ports
nao_ip = "127.0.0.1"
nao_port = 9559

nao_ip2 = "127.0.0.1"
nao_port2 = 9560

# Connecting the NAO robot at the given address
# to modules that we can call
try:
    motionProxy = ALProxy("ALMotion", nao_ip, nao_port)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e

try:
    motionProxy2 = ALProxy("ALMotion", nao_ip2, nao_port2)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e

# First, set Body Stiffness to ON.
motionProxy.setStiffnesses("Body", 1.0)
motionProxy2.setStiffnesses("Body", 1.0)

# print motionProxy.getBrokerName()
# print motionProxy2.getBrokerName()


# seek(motionProxy, ball_location)


# post lets us execute commands at the same time
# without it one robot would move and afterwards the other robot would move
# motionProxy.post.moveTo(1, 0, 20)
# motionProxy2.post.moveTo(1, 0, 20)

# Main Loop
try:
    while True:
    	#Parameters:	
		#    useSensors - If true, use the MRE sensor values
		#Returns:	
		#	A vector containing the World Absolute Robot Position. 
		#	(Absolute Position X, Absolute Position Y, Absolute Angle Theta (Wz)).
		location = motionProxy2.getRobotPosition(False)
		print location
		motionProxy2.post.moveTo(1, 0, 0)
		time.sleep(1)


# Exit Behaviour
except KeyboardInterrupt:
	print
	print "Interrupted by user, shutting down"
	sys.exit(0)



