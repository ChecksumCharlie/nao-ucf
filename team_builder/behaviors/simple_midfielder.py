from util import parameters


class LogicFor:
    def __init__(self, RobotGiven):
        self.player = RobotGiven

    def update(self):
        
        parameters.wrapFSM(self)


    def runFSM(self): 
            # new value
            RedBall = self.player.getRedBall()
            # behavior logic
            if (self.player.hasFallen()):
                self.player.initStance()
            
            elif (len(RedBall)>0):
                if (RedBall[0]<300):
                    self.player.walk(0.1)
                elif (RedBall[0]>400):
                    self.player.walk(-0.1)
                else:
                    self.player.walk(0.0)
            else:
                self.player.walk(0.5)
