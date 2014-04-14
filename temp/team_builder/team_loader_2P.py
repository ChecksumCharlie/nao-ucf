import sys
import time
from multiprocessing import Process

from util import nao_robot as robot
from behaviors import simple_midfielder
from behaviors import simple_goalie

# Robot ip address and port
IP = "127.0.0.1"
PORT = 9560

RobotBlue = robot.CreateRobot(IP, PORT)
RobotBlueLogic = simple_goalie.LogicFor(RobotBlue)


IP = "127.0.0.1"
PORT = 9559

RobotPink = robot.CreateRobot(IP, PORT)
RobotPinkLogic = simple_midfielder.LogicFor(RobotPink)

           

while (True):
    p = Process(target=RobotPinkLogic.update())
    p.start()
    p.join()

    p = Process(target=RobotBlueLogic.update())
    p.start()
    p.join()
 

# Safe Exit for Webots' sake
sys.exit(0)
