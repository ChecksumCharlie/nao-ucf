'''
Created on Apr 1, 2014

@author: Sarah
'''
game_in_action = True

Offender = 1
Defender = 2
Goalie = 3

import Offender
from Robot import Robot
    
IP = "127.0.0.1"
PORT = 9560 # List of these...
Captain = Robot ( IP, PORT )

Captain.Initialize (Offender())
print "Im Alive"
#Captain.Set (Offender)
while game_in_action:
    Captain.Run ()
    #some determination algorithm
    #Captain.Set(Defender)
    #some game state calculation 
    game_in_action = False #or true...?

Captain.Dispose ()