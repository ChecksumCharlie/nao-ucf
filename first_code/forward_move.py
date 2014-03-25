#Chris Cassian Olschewski
#Definding player module

import sys
import time
from naoqi import ALProxy


IP = "127.0.0.1"
PORT = 9560

# Connecting motion module to the NAO robot that we can call
motion = ALProxy("ALMotion", IP, PORT)
motion.setStiffnesses("Body", 1.0)
motion.moveInit()


# Main Loop
try:  
        while True:
            nao_move = motion.post.moveTo(3, 0, 0)
            motion.wait(nao_move, 0)
            
# Exit Behaviour
except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        sys.exit(0)
    
