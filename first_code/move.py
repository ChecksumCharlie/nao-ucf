# Program 1: move 3 meters forward

import sys
import time
from naoqi import ALProxy

# Robot ip address and port
IP = "127.0.0.1"
PORT = 9560

# Connecting the NAO robot at the given address 
#to a motion module that we can call
motion = ALProxy("ALMotion", IP, PORT)
# Release the body stiffness, when 0 robot won't move
motion.setStiffnesses("Body", 1.0)
# Move the robot to his Initialize position
motion.moveInit()

# Forward move, and waiting till finished
# moveTo(x, y, theta)
#    x – Distance along the X axis in meters.
#    y – Distance along the Y axis in meters.
#    theta – Rotation around the Z axis in radians [-3.1415 to 3.1415].
#
nao_move = motion.post.moveTo(3, 0, 0)
motion.wait(nao_move, 0)
            
# Safe Exit
sys.exit(0)
    
