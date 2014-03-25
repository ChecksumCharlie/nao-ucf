# Program 2: tracking the ball with NAO's head, using postures

import sys
import time
from naoqi import ALProxy

# Robot ip address and port
nao_ip = "127.0.0.1"
nao_port = 9560

# Connecting the NAO robot at the given address
# to modules that we can call
motionProxy = ALProxy("ALMotion", nao_ip, nao_port)
postureProxy = ALProxy("ALRobotPosture", nao_ip, nao_port)
redBallTracker = ALProxy("ALRedBallTracker", nao_ip, nao_port)


# Release the body stiffness, when 0 robot won't move
motionProxy.setStiffnesses("Body", 1.0)

# Send NAO to Pose Init
postureProxy.goToPosture("StandInit", 0.5)

# Activate ball tracking by head
redBallTracker.startTracker()

# Ball tracker sometimes has difficulty loading    
time.sleep(4.0)
# Run tracking for 10 secs
time.sleep(10.0)

# Deactivate tracking of ball
redBallTracker.stopTracker()

# Safe Exit
sys.exit(0)