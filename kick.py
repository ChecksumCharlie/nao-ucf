def rightKick(self, prime, execute, coolDown):

    # Legs are constrained fixed
    stateName  = "Fixed"
    supportLeg = "Legs"
    self.motionProxy.wbFootState(stateName, supportLeg)

    # Constraint Balance Motion
    isEnable   = True
    supportLeg = "Legs"
    motionProxy.wbEnableBalanceConstraint(isEnable, supportLeg)

    # Com go to LLeg
    supportLeg = "LLeg"
    duration   = 2.0
    motionProxy.wbGoToBalance(supportLeg, duration)

    # RLeg is free
    stateName  = "Free"
    supportLeg = "RLeg"
    motionProxy.wbFootState(stateName, supportLeg)

    # RLeg is optimized
    effectorName = "RLeg"
    axisMask     = 63
    space        = motion.FRAME_ROBOT


    # Motion of the RLeg
    dx      = 0.05
    dz      = 0.05
    dwy     = 5.0*math.pi/180.0


    times   = [prime, execute, coolDown]
    isAbsolute = False

    targetList = [
        [-dx, 0.0, dz, 0.0, +dwy, 0.0],
        [+dx, 0.0, dz, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

    motionProxy.positionInterpolation(effectorName, space, targetList,
                                axisMask, times, isAbsolute)


def leftKick(self, prime, execute, coolDown):
    
    # Legs are constrained fixed
    stateName  = "Fixed"
    supportLeg = "Legs"
    self.motionProxy.wbFootState(stateName, supportLeg)
    
    # Constraint Balance Motion
    isEnable   = True
    supportLeg = "Legs"
    motionProxy.wbEnableBalanceConstraint(isEnable, supportLeg)
    
    # Com go to LLeg
    supportLeg = "LLeg"
    duration   = 2.0
    motionProxy.wbGoToBalance(supportLeg, duration)
    
    # RLeg is free
    stateName  = "Free"
    supportLeg = "RLeg"
    motionProxy.wbFootState(stateName, supportLeg)
    
    # RLeg is optimized
    effectorName = "RLeg"
    axisMask     = 63
    space        = motion.FRAME_ROBOT

    # Motion of the RLeg
    dx      = 0.05
    dz      = 0.05
    dwy     = 5.0*math.pi/180.0
    
    
    times   = [prime, execute, coolDown]
    isAbsolute = False

    targetList = [
        [-dx, 0.0, dz, 0.0, +dwy, 0.0],
        [+dx, 0.0, dz, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

    motionProxy.positionInterpolation(effectorName, space, targetList,
                                  axisMask, times, isAbsolute)
