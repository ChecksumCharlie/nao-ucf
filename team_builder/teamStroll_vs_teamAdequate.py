import sys
import time
from threading import Thread
from util import nao_robot as robot

# Import robot behaviors
from behaviors import stroll_goalie
from behaviors import stroll_midfielder
from behaviors import stroll_striker
from behaviors import teamAdequate_player
from behaviors import simple_goalie
from behaviors import teamLadder_midfielder
from behaviors import static_player

# Load robots and their behaviors
RobotBlueGoalie = robot.CreateRobot("127.0.0.1", 9559) 
RobotBlueGoalieLogic = static_player.LogicFor(RobotBlueGoalie)

RobotBlueMidfielder = robot.CreateRobot("127.0.0.1", 9560)
RobotBlueMidfielderLogic = static_player.LogicFor(RobotBlueMidfielder)

RobotBlueStriker = robot.CreateRobot("127.0.0.1", 9561)
RobotBlueStrikerLogic = teamLadder_midfielder.LogicFor(RobotBlueStriker)

RobotPinkGoalie = robot.CreateRobot("127.0.0.1", 9562)
RobotPinkGoalieLogic = static_player.LogicFor(RobotPinkGoalie) 

RobotPinkMidfielder = robot.CreateRobot("127.0.0.1", 9563)
RobotPinkMidfielderLogic = static_player.LogicFor(RobotPinkMidfielder)

RobotPinkStriker = robot.CreateRobot("127.0.0.1", 9564)
RobotPinkStrikerLogic = teamAdequate_player.LogicFor(RobotPinkStriker)

print "All Robots and Logic loaded!"


# # Run robot FSMs concurrently
p1 = Thread(target=RobotBlueGoalieLogic.update)
p2 = Thread(target=RobotBlueMidfielderLogic.update)
p3 = Thread(target=RobotBlueStrikerLogic.update)

p4 = Thread(target=RobotPinkGoalieLogic.update)
p5 = Thread(target=RobotPinkMidfielderLogic.update)
p6 = Thread(target=RobotPinkStrikerLogic.update)

p1.start()
p2.start()
p3.start()
print "Blue Team Go!"

p4.start()
p5.start()
p6.start()
print "Pink Team Go!"

p1.join()
p2.join()
p3.join()

p4.join()
p5.join()
p6.join()

'''
Unreachable...
RobotBlueStrikerLogic.__del__()
RobotBlueMidfielderLogic.__del__()
RobotBlueGoalieLogic.__del__()

RobotPinkStrikerLogic.__del__()
RobotPinkMidfielderLogic.__del__()
RobotPinkGoalieLogic.__del__()
'''
# Safe Exit for Webots' sake
sys.exit(0)
