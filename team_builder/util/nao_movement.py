import motion
from naoqi import ALProxy
import math
import time

class RobotLegs:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT

        self.motionProxy = ALProxy("ALMotion", self.IP, self.PORT)
        self.postureProxy = ALProxy("ALRobotPosture", self.IP, self.PORT)

        self.motionProxy.stiffnessInterpolation("Body", 1.0, 1.0)

    def walk(self, value):
        self.motionProxy.setWalkTargetVelocity(1.0,0.0,value,1.0,
                [#LEFT
                ["MaxStepX", 0.07],
                #maxStepYRight,
                ["MaxStepTheta", 0.349],
                ["MaxStepFrequency", 1],
                ["StepHeight", 0.015],
                ["TorsoWx", 0.0],
                ["TorsoWy", 0.0]],
                [#RIGHT
                ["MaxStepX", 0.7],
                #maxStepYLeft,
                ["MaxStepTheta", 0.349],
                ["MaxStepFrequency", 1],
                ["StepHeight", 0.015],
                ["TorsoWx", 0.0], 
                ["TorsoWy", 0.0]])

    def stop(self):
        self.motionProxy.setWalkTargetVelocity(0.0,0.0,0,0.0,
                [#LEFT
                ["MaxStepX", 0.07],
                #maxStepYRight,
                ["MaxStepTheta", 0.349],
                ["MaxStepFrequency", 1],
                ["StepHeight", 0.015],
                ["TorsoWx", 0.0],
                ["TorsoWy", 0.0]],
                [#RIGHT
                ["MaxStepX", 0.7],
                #maxStepYLeft,
                ["MaxStepTheta", 0.349],
                ["MaxStepFrequency", 1],
                ["StepHeight", 0.015],
                ["TorsoWx", 0.0], 
                ["TorsoWy", 0.0]])

    def sidestep(self, value):
        self.motionProxy.setWalkTargetVelocity(0.0,value,0.0,1.0,
                [#LEFT
                ["MaxStepX", 0.07],
                #maxStepYRight,
                ["MaxStepTheta", 0.349],
                ["MaxStepFrequency", 1],
                ["StepHeight", 0.015],
                ["TorsoWx", 0.0],
                ["TorsoWy", 0.0]],
                [#RIGHT
                ["MaxStepX", 0.7],
                #maxStepYLeft,
                ["MaxStepTheta", 0.349],
                ["MaxStepFrequency", 1],
                ["StepHeight", 0.015],
                ["TorsoWx", 0.0], 
                ["TorsoWy", 0.0]])

    def killWalk(self):
        self.motionProxy.stopWalk()

    def leftKick(self, prime, execute, cool_down):

        # Activate Whole Body Balancer
        isEnabled  = True
        self.motionProxy.wbEnable(isEnabled)

        # Legs are constrained fixed
        stateName  = "Fixed"
        supportLeg = "Legs"
        self.motionProxy.wbFootState(stateName, supportLeg)

        # Constraint Balance Motion
        isEnable   = True
        supportLeg = "Legs"
        self.motionProxy.wbEnableBalanceConstraint(isEnable, supportLeg)

        # Com go to LLeg
        supportLeg = "LLeg"
        duration   = 2.0
        self.motionProxy.wbGoToBalance(supportLeg, duration)

        # RLeg is free
        stateName  = "Free"
        supportLeg = "RLeg"
        self.motionProxy.wbFootState(stateName, supportLeg)

        # RLeg is optimized
        effectorName = "RLeg"
        axisMask     = 63
        space        = motion.FRAME_ROBOT


        # Motion of the RLeg
        dx      = 0.05                 # translation axis X (meters)
        dz      = 0.05                 # translation axis Z (meters)
        dwy     = 5.0*math.pi/180.0    # rotation axis Y (radian)


        times   = [prime, execute, cool_down]
        isAbsolute = False

        targetList = [
          [-dx, 0.0, dz, 0.0, +dwy, 0.0],
          [+dx, 0.0, dz, 0.0, 0.0, 0.0],
          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

    

        # Example showing how to Enable Effector Control as an Optimization
        isActive     = False
        self.motionProxy.wbEnableEffectorOptimization(effectorName, isActive)

        # Com go to LLeg
        supportLeg = "RLeg"
        duration   = 2.0
        self.motionProxy.wbGoToBalance(supportLeg, duration)

        # RLeg is free
        stateName  = "Free"
        supportLeg = "LLeg"
        self.motionProxy.wbFootState(stateName, supportLeg)

        effectorName = "LLeg"
        self.motionProxy.positionInterpolation(effectorName, space, targetList,
                                    axisMask, times, isAbsolute)

        time.sleep(1.0)

        # Deactivate Head tracking
        isEnabled    = False
        self.motionProxy.wbEnable(isEnabled)


    def rightKick(self, prime, execute, cool_down):
        
        # Activate Whole Body Balancer
        isEnabled  = True
        self.motionProxy.wbEnable(isEnabled)

        # Legs are constrained fixed
        stateName  = "Fixed"
        supportLeg = "Legs"
        self.motionProxy.wbFootState(stateName, supportLeg)

        # Constraint Balance Motion
        isEnable   = True
        supportLeg = "Legs"
        self.motionProxy.wbEnableBalanceConstraint(isEnable, supportLeg)

        # Com go to LLeg
        supportLeg = "LLeg"
        duration   = 2.0
        self.motionProxy.wbGoToBalance(supportLeg, duration)

        # RLeg is free
        stateName  = "Free"
        supportLeg = "RLeg"
        self.motionProxy.wbFootState(stateName, supportLeg)

        # RLeg is optimized
        effectorName = "RLeg"
        axisMask     = 63
        space        = motion.FRAME_ROBOT


        # Motion of the RLeg
        dx      = 0.05                 # translation axis X (meters)
        dz      = 0.05                 # translation axis Z (meters)
        dwy     = 5.0*math.pi/180.0    # rotation axis Y (radian)


        times   = [1.0, 1.05, 2.5]
        isAbsolute = False

        targetList = [
          [-dx, 0.0, dz, 0.0, +dwy, 0.0],
          [+dx, 0.0, dz, 0.0, 0.0, 0.0],
          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

        #proxy.positionInterpolation(effectorName, space, targetList,
        #                             axisMask, times, isAbsolute)


        # Example showing how to Enable Effector Control as an Optimization
        isActive     = False
        self.motionProxy.wbEnableEffectorOptimization(effectorName, isActive)

        # Com go to LLeg
        supportLeg = "RLeg"
        duration   = 2.0
        self.motionProxy.wbGoToBalance(supportLeg, duration)

        # RLeg is free
        stateName  = "Free"
        supportLeg = "LLeg"
        self.motionProxy.wbFootState(stateName, supportLeg)

        effectorName = "LLeg"
        self.motionProxy.positionInterpolation(effectorName, space, targetList,
                                    axisMask, times, isAbsolute)

        time.sleep(1.0)

        # Deactivate Head tracking
        isEnabled    = False
        self.motionProxy.wbEnable(isEnabled)

    def getAngle(self, string):
        return self.motionProxy.getAngles(string, False)

    def setHeadAngle(self, angle, string):
        self.motionProxy.setStiffnesses("Head", 1.0)
        angs = [math.radians(angle)]
        self.motionProxy.angleInterpolation(string, angs, 1, True)

    def simple180(self):        

        x  = 0
        y  = 0
        # pi anti-clockwise (180 degrees)
        theta = 3.1418

        self.motionProxy.moveTo(x, y, theta)


    def simple90left(self):
        x  = 0
        y  = 0
        # pi anti-clockwise (180 degrees)
        theta = 1.5709 

        self.motionProxy.moveTo(x, y, theta)

    def simple90right(self):
        x  = 0
        y  = 0
        # pi anti-clockwise (180 degrees)
        theta = -1.5709 

        self.motionProxy.moveTo(x, y, theta)

    def initStance(self):
        self.postureProxy.goToPosture("StandInit", 0.5)