from multiprocessing import Process
import sys
import time

from util import nao_robot as robot, parameters as param


class LogicFor:
    def __init__(self, RobotGiven):
        self.player = RobotGiven

    def update(self):
        
        param.wrapFSM(self)


    def runFSM(self): 
        
        self.player.initStance()
