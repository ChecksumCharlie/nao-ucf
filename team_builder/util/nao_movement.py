
from naoqi import ALProxy



class RobotLegs:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT

        self.motionProxy = ALProxy("ALMotion", self.IP, self.PORT)

        self.motionProxy.stiffnessInterpolation("Body", 1.0, 1.0)

    def walk(self, value=0):
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

