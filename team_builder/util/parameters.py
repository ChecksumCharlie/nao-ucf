import time


def wrapFSM(self):
    ###
    # Change timeStep to increase or decrease the duration each state of the Logic FSM lasts
    ###
    # float required
    timeStep = 1.0

    self.runFSM()
    
    timeDiff = time.time()-self.player.timeMemory    
    
    if (timeDiff<timeStep):
        time.sleep(timeStep-timeDiff)

    self.player.timeMemory = time.time()
    