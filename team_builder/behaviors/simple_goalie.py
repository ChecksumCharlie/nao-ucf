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
            if (len(RedBall)>0):
                if (RedBall[0]<300):
                    self.player.sidestep(1.0)
                elif (RedBall[0]>400):
                    self.player.sidestep(-1.0)
                else:
                    self.player.sidestep(0.0)
            else:
                self.player.sidestep(0.0)
