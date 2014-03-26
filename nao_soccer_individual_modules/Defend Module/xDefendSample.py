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
