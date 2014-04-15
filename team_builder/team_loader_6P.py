import sys
import time
from multiprocessing import Process
from util import nao_robot as robot

# Import robot behaviors
from behaviors import simple_midfielder
from behaviors import simple_goalie
from behaviors import simple_striker
from behaviors import static_player
from behaviors import teamLadder_goalie
from behaviors import template_player

# Load robots and their behaviors
RobotBlueGoalie = robot.CreateRobot("127.0.0.1", 9559)
RobotBlueGoalieLogic = template_player.LogicFor(RobotBlueGoalie)

RobotBlueMidfielder = robot.CreateRobot("127.0.0.1", 9560)
RobotBlueMidfielderLogic = static_player.LogicFor(RobotBlueMidfielder)

RobotBlueStriker = robot.CreateRobot("127.0.0.1", 9561)
RobotBlueStrikerLogic = static_player.LogicFor(RobotBlueStriker)

RobotPinkGoalie = robot.CreateRobot("127.0.0.1", 9562)
RobotPinkGoalieLogic = static_player.LogicFor(RobotPinkGoalie) 

RobotPinkMidfielder = robot.CreateRobot("127.0.0.1", 9563)
RobotPinkMidfielderLogic = static_player.LogicFor(RobotPinkMidfielder)

RobotPinkStriker = robot.CreateRobot("127.0.0.1", 9564)
RobotPinkStrikerLogic = static_player.LogicFor(RobotPinkStriker)  

print "All Robots and Logic loaded!"

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
