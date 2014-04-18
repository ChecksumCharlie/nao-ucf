import sys
import time
from threading import Thread
from util import nao_robot as robot

# Import robot behaviors
from behaviors import static_player
from behaviors import teamLadder_goalie
from behaviors import teamLadder2_midfielder
from behaviors import teamAdequate_player


# Load robots and their behaviors
RobotBlueGoalie = robot.CreateRobot("127.0.0.1", 9559) 
RobotBlueGoalieLogic = teamLadder_goalie.LogicFor(RobotBlueGoalie)

RobotBlueMidfielder = robot.CreateRobot("127.0.0.1", 9560)
RobotBlueMidfielderLogic = teamLadder2_midfielder.LogicFor(RobotBlueMidfielder)

# RobotBlueStriker = robot.CreateRobot("127.0.0.1", 9561)
# RobotBlueStrikerLogic = simple_midfielder.LogicFor(RobotBlueStriker)

# RobotPinkGoalie = robot.CreateRobot("127.0.0.1", 9562)
# RobotPinkGoalieLogic = simple_goalie.LogicFor(RobotPinkGoalie) 

# RobotPinkMidfielder = robot.CreateRobot("127.0.0.1", 9563)
# RobotPinkMidfielderLogic = simple_midfielder.LogicFor(RobotPinkMidfielder)

# RobotPinkStriker = robot.CreateRobot("127.0.0.1", 9564)
# RobotPinkStrikerLogic = simple_midfielder.LogicFor(RobotPinkStriker)  

print "All Robots and Logic loaded!"

# Run robot FSMs concurrently

p1 = Thread(target=RobotBlueGoalieLogic.update)
p2 = Thread(target=RobotBlueMidfielderLogic.update)
# p3 = Thread(target=RobotBlueStrikerLogic.update)

# p4 = Thread(target=RobotPinkGoalieLogic.update)
# p5 = Thread(target=RobotPinkMidfielderLogic.update)
# p6 = Thread(target=RobotPinkStrikerLogic.update)

p1.start()
p2.start()
# p3.start()
# print "Blue Team Go!"

# p4.start()
# p5.start()
# p6.start()
print "Pink Team Go!"

p1.join()
p2.join()
# p3.join()

# p4.join()
# p5.join()
# p6.join()

 


# Safe Exit for Webots' sake
sys.exit(0)
