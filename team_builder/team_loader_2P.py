from multiprocessing import Process
import sys
import time

from behaviors import simple_goalie, simple_midfielder, simple_striker
from util import nao_robot as robot


# Robot ip address and port
IP = "127.0.0.1"
PORT = 9561

RobotBlue = robot.CreateRobot(IP, PORT)
RobotBlueLogic = simple_striker.LogicFor(RobotBlue)


# IP = "127.0.0.1"
# PORT = 9559
# 
# RobotPink = robot.CreateRobot(IP, PORT)
# RobotPinkLogic = simple_midfielder.LogicFor(RobotPink)

while (True):
    p = Process(target=RobotBlueLogic.update())
    p.start()
    p.join()
# 
#     p = Process(target=RobotBlueLogic.update())
#     p.start()
#     p.join()
 

# Safe Exit for Webots' sake
sys.exit(0)
