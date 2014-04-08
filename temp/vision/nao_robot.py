import nao_vision as vision
import nao_movement as movement

class CreateRobot:
    def __init__(self, IP, PORT):
    	self.IP = IP
    	self.PORT = PORT

    	self.RobotEyes = vision.RobotEyes(self.IP, self.PORT)
    	self.RobotLegs = movement.RobotLegs(self.IP, self.PORT)

    def walk(self, value=0):
    	self.RobotLegs.walk(value)

    def stop(self):
    	self.RobotLegs.stop()

    def getImage(self):
    	self.RobotEyes.getImage()

    def getOrangeBall(self):
    	return self.RobotEyes.getOrangeBall()

    def getYellowGoal(self):
    	return self.RobotEyes.getYellowGoal()

    def getBlueGoal(self):
    	return self.RobotEyes.getBlueGoal()