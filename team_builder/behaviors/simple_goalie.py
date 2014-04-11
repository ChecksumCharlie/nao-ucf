import sys
import time
from multiprocessing import Process

from util import nao_robot as robot

class LogicFor:
    def __init__(self, RobotGiven):
        self.player = RobotGiven

    def update(self):
            # new value
            OrangeBall = self.player.getOrangeBall()
            # behavior logic
            if (OrangeBall!=None):
                if (OrangeBall[0]<300):
                    self.player.sidestep(1.0)
                elif (OrangeBall[0]>400):
                    self.player.sidestep(-1.0)
                else:
                    self.player.sidestep(0.0)
            else:
                self.player.sidestep(0.0)
