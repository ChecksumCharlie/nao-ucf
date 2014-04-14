'''
Created on Apr 6, 2014

@author: Sarah
'''

from Behavior import Behavior

class Defender(Behavior):

    def __init__(self, params):
        Behavior.__init__(self)
    
    def Run (self, robot):
        print "I'm ready, defending UCF's goal"

        key = "Device/SubDeviceList/HeadYaw/Position/Sensor/Value"
        while True:
            # Get head position sensor value
            value = self.memoryProxy.post.getData(key)
            print value
            # Check if move to left
            if value>=0.1:
                self.motionProxy.post.setWalkTargetVelocity(0.0, 1.0, 0.0, 1.0)
            # Check if move to right
            elif value<=-0.1:
                self.motionProxy.post.setWalkTargetVelocity(0.0, -1.0, 0.0, 1.0)
            # Check if need to stop
            else:
                self.motionProxy.post.setWalkTargetVelocity(0.0, 0.0, 0.0, 0.0)