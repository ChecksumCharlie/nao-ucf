import sys
from multiprocessing import Process
from util import nao_robot as robot

# Import robot behaviors
from behaviors import simple_midfielder
from behaviors import simple_goalie
from behaviors import simple_offender

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
bg = Process(target=RobotBlueGoalieLogic.update())
bg.start()

bm = Process(target=RobotBlueMidfielderLogic.update())
bm.start()

bs = Process(target=RobotBlueStrikerLogic.update())
bs.start()

pg = Process(target=RobotPinkGoalieLogic.update())
pg.start()

pm = Process(target=RobotPinkMidfielderLogic.update())
pm.start()

ps = Process(target=RobotPinkStrikerLogic.update())
ps.start()

bg.terminate()
bm.terminate()
bs.terminate()
pg.terminate()
pm.terminate()
ps.terminate()

bg.join()
bm.join()
bs.join()
pg.join()
pm.join()
ps.join()

RobotPinkGoalie.__del__ ()
RobotPinkMidfielder.__del__ ()
RobotPinkStriker.__del__ ()
RobotBlueGoalie.__del__ ()
RobotBlueMidfielder.__del__ ()
RobotBlueStriker.__del__ ()

# Safe Exit for Webots' sake
sys.exit(0)
