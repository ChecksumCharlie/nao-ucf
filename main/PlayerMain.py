'''
Created on Apr 6, 2014

@author: Sarah
'''

Offender = "Offender"
Defender = "Defender"
Goalie = "Goalie"

from Robot import Robot
    
IP = "127.0.0.1"
PORT = 0000 #OTHER PORT
Player = Robot ( IP, PORT )

Player.Initialize ( Offender () )

print "Im Alive"

Player.Run(None)
Player.Dispose()