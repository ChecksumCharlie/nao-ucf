from util import parameters as param


class LogicFor:
    def __init__(self, RobotGiven):
        self.player = RobotGiven

    def update(self):
        
        param.wrapFSM(self)


    def runFSM(self):            

        if (True):
            print "This is my only state."
