#Chris Cassian Olschewski
#Definding player module

import sys
import time
from naoqi import ALProxy


IP = "127.0.0.1"
PORT = 9560

# Connecting motion module to the NAO robot that we can call
motion = ALProxy("ALMotion", IP, PORT)

# 
motion.setStiffnesses("Body", 1.0)


# Move robot 3 meters forward with ALMotion proxy module
motion.post.moveTo(3, 0, 0)
            
# Safe Exit for Webots' sake
sys.exit(0)
    
