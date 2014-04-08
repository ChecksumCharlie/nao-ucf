import sys
import time
from multiprocessing import Process

import nao_robot as robot

# Robot ip address and port
IP = "127.0.0.1"
PORT = 9560

RobotBlue = robot.CreateRobot(IP, PORT)

IP = "127.0.0.1"
PORT = 9559

RobotPink = robot.CreateRobot(IP, PORT)

# RobotNo1.walk(1)
# RobotNo2.walk(1)

def blue_logic(RobotBlue):
    # while (True):
        if (RobotBlue.getYellowGoal()==None and RobotBlue.getOrangeBall()!=None):
            if (RobotBlue.getOrangeBall()[0]<300):
                RobotBlue.walk(-0.1)
            elif (RobotBlue.getOrangeBall()[0]>300):
                RobotBlue.walk(0.1)
            else:
                RobotBlue.walk(0.0)
        elif (RobotBlue.getYellowGoal()!=None):
            RobotBlue.walk(0)
            RobotBlue.walk(0)
            RobotBlue.walk(0)
            time.sleep(5)
            RobotBlue.walk(0.7)
        else:
            RobotBlue.walk(0.7)
        

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

def print_hello():
    print "hello"
            

while (True):
    p = Process(target=pink_logic, args=(RobotBlue,))
    p.start()
    p.join()

    p = Process(target=pink_logic, args=(RobotPink,))
    p.start()
    p.join()

# pool = Pool()
# # evaluate  asynchronously

# pool.apply_async(blue_logic(RobotBlue)) 
# pool.apply_async(print_hello())    



# Safe Exit for Webots' sake
sys.exit(0)
