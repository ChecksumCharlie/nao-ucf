import sys
import time

import nao_robot as robot

# Robot ip address and port
IP = "127.0.0.1"
PORT = 9560

RobotNo1 = robot.CreateRobot(IP, PORT)

IP = "127.0.0.1"
PORT = 9559

RobotNo2 = robot.CreateRobot(IP, PORT)

# RobotNo1.walk(1)
# RobotNo2.walk(1)

# RobotNo2.stop()
# RobotNo1.stop()

print RobotNo1.getOrangeBall()
print RobotNo2.getOrangeBall()


# Safe Exit for Webots' sake
sys.exit(0)
