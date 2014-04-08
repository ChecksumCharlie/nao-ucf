'''
Created on Apr 6, 2014

@author: Sarah
'''

from Behavior import Behavior

class Defender(Behavior):

    def __init__(self, params):
        Behavior.__init__(self)
    
    def run (self, robot):
        