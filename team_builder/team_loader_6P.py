from multiprocessing import Process
import sys

from behaviors import simple_goalie, simple_midfielder, simple_offender
from util import nao_robot as robot

# Import robot behaviors
# Load robots and their behaviors
RobotBlueGoalie = robot.CreateRobot("127.0.0.1", 9559)
RobotBlueGoalieLogic = simple_goalie.LogicFor(RobotBlueGoalie)

RobotBlueMidfielder = robot.CreateRobot("127.0.0.1", 9560)
RobotBlueMidfielderLogic = simple_midfielder.LogicFor(RobotBlueMidfielder)

RobotBlueStriker = robot.CreateRobot("127.0.0.1", 9561)
RobotBlueStrikerLogic = simple_offender.LogicFor(RobotBlueStriker)

RobotPinkGoalie = robot.CreateRobot("127.0.0.1", 9562)
RobotPinkGoalieLogic = simple_goalie.LogicFor(RobotPinkGoalie) 

RobotPinkMidfielder = robot.CreateRobot("127.0.0.1", 9563)
RobotPinkMidfielderLogic = simple_midfielder.LogicFor(RobotPinkMidfielder)

RobotPinkStriker = robot.CreateRobot("127.0.0.1", 9564)
RobotPinkStrikerLogic = simple_midfielder.LogicFor(RobotPinkStriker)  

# Run robot FSMs concurrently
b = Process(target=RobotBlueGoalieLogic.update())
b.start()
b.join()

b = Process(target=RobotBlueMidfielderLogic.update())
b.start()
b.join()

b = Process(target=RobotBlueStrikerLogic.update())
b.start()
b.join()

b = Process(target=RobotPinkGoalieLogic.update())
b.start()
b.join()

b = Process(target=RobotPinkMidfielderLogic.update())
b.start()
b.join()

b = Process(target=RobotPinkStrikerLogic.update())
b.start()
b.join()

#bg.join()
#bm.join()
#bs.join()
#pg.join()
#pm.join()
#ps.join()

# Safe Exit for Webots' sake
sys.exit(0)
