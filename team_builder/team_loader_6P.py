import sys
import time
from multiprocessing import Process
from util import nao_robot as robot

# Import robot behaviors
from behaviors import simple_midfielder
from behaviors import simple_goalie
from behaviors import simple_striker

# Load robots and their behaviors
RobotBlueGoalie = robot.CreateRobot("127.0.0.1", 9559)
RobotBlueGoalieLogic = simple_goalie.LogicFor(RobotBlueGoalie)

RobotBlueMidfielder = robot.CreateRobot("127.0.0.1", 9560)
RobotBlueMidfielderLogic = simple_midfielder.LogicFor(RobotBlueMidfielder)

RobotBlueStriker = robot.CreateRobot("127.0.0.1", 9561)
RobotBlueStrikerLogic = simple_stricker.LogicFor(RobotBlueStriker)

RobotPinkGoalie = robot.CreateRobot("127.0.0.1", 9562)
RobotPinkGoalieLogic = simple_goalie.LogicFor(RobotPinkGoalie) 

RobotPinkMidfielder = robot.CreateRobot("127.0.0.1", 9563)
RobotPinkMidfielderLogic = simple_midfielder.LogicFor(RobotPinkMidfielder)

RobotPinkStriker = robot.CreateRobot("127.0.0.1", 9564)
RobotPinkStrikerLogic = simple_midfielder.LogicFor(RobotPinkStriker)  

# Run robot FSMs concurrently
while (True):
    p = Process(target=RobotBlueGoalieLogic.update())
    p.start()
    p.join()

    p = Process(target=RobotBlueMidfielderLogic.update())
    p.start()
    p.join()

    p = Process(target=RobotBlueStrikerLogic.update())
    p.start()
    p.join()

    p = Process(target=RobotPinkGoalieLogic.update())
    p.start()
    p.join()

    p = Process(target=RobotPinkMidfielderLogic.update())
    p.start()
    p.join()

    p = Process(target=RobotPinkStrikerLogic.update())
    p.start()
    p.join()
 
# Safe Exit for Webots' sake
sys.exit(0)
