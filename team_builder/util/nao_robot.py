import time

import nao_vision as vision
import nao_movement as movement

class CreateRobot:
    def __init__(self, IP, PORT):
    	self.IP = IP
    	self.PORT = PORT

        self.timeMemory = time.time()

    	self.RobotEyes = vision.RobotEyes(self.IP, self.PORT)
    	self.RobotLegs = movement.RobotLegs(self.IP, self.PORT)

        self.motionProxy = self.RobotLegs.motionProxy
        self.postureProxy = self.RobotLegs.postureProxy
        self.memoryProxy = self.RobotLegs.memoryProxy
        # self.sonarProxy = self.RobotLegs.sonarProxy


    def walk(self, value=0):
    	self.RobotLegs.walk(value)

    def walk2(self, x, y, theta):
        self.RobotLegs.walk2(x, y, theta)

    def stop(self):
    	self.RobotLegs.stop()

    def displayImage(self):
    	self.RobotEyes.displayImage()

    def getRedBall(self):
    	return self.RobotEyes.getRedBall()

    def getYellowGoal(self):
    	return self.RobotEyes.getYellowGoal()

    def getBlueGoal(self):
    	return self.RobotEyes.getBlueGoal()

    def getBluePlayers(self):
        return self.RobotEyes.getBluePlayers()

    def getPinkPlayers(self):
        return self.RobotEyes.getPinkPlayers()   

    def sidestep(self, value):
        self.RobotLegs.sidestep(value)

    def killWalk(self):
        self.RobotLegs.killWalk()

    def leftKick(self, prime, execute, cool_down):
        self.RobotLegs.leftKick(prime, execute, cool_down)

    def rightKick(self, prime, execute, cool_down):
        self.RobotLegs.rightKick(prime, execute, cool_down)    

    def getAngle(self, string):
        return self.RobotLegs.getAngle(string)   

    def setHeadAngle(self, angle, string):
        self.RobotLegs.setHeadAngle(angle, string)

    def simple180(self):
        self.RobotLegs.simple180()

    def simple90left(self):
        self.RobotLegs.simple90left()

    def simple90right(self):
        self.RobotLegs.simple90right()

    def getYellowGoalHeight(self):
        return self.RobotEyes.getYellowGoalHeight()

    def getBlueGoalHeight(self):
        return self.RobotEyes.getBlueGoalHeight()

    def getRedBall2(self):
        return self.RobotEyes.getRedBall2()
        
    def getBlueGoal2(self):
        return self.RobotEyes.getBlueGoal2()

    def getYellowGoal2(self):
        return self.RobotEyes.getYellowGoal2()
        
    def getBluePlayers2(self):
        return self.RobotEyes.getBluePlayers2()
        
    def getPinkPlayers2(self):
        return self.RobotEyes.getPinkPlayers2()

    def initStance(self):
        self.RobotLegs.initStance()

    def hasFallen(self):
        return self.RobotLegs.hasFallen()

    def getYellowGoalWidth(self):        
        return self.RobotEyes.getYellowGoalWidth()

    def getBlueGoalWidth(self):
        return self.RobotEyes.getBlueGoalWidth()

    # def sonarLeftDist(self):
    #     return self.RobotLegs.sonarLeftDist()

    # def sonarRightDist(self):
    #     return self.RobotLegs.sonarRightDist()
       
