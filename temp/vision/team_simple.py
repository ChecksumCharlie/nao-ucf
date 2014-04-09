import sys
import time
from multiprocessing import Process

import nao_robot as robot

def pink_logic(RobotPink):
    # while (True):
        # new value
        OrangeBall = RobotPink.getOrangeBall()
        # behavior logic
        if (OrangeBall!=None):
            if (OrangeBall[0]<300):
                RobotPink.walk(0.1)
            elif (OrangeBall[0]>300):
                RobotPink.walk(-0.1)
            else:
                RobotPink.walk(0.0)
        else:
            RobotPink.walk(0.5)
