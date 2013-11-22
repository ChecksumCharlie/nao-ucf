'''
Created on Nov 10, 2013

@author: Astrid
'''

import motion;
import math;
import time;

from util import state_machine;
from util import state;

class NaoBody(object):
    naoBody_sm = None;

    def __init__(self, motion, posture, redBallTracker):
        self.naoBody_sm = state_machine.StateMachine({'name':'bodyIdle', 'handle': BodyIdle(motion, posture)});
        self.naoBody_sm.addState({'name':'bodyChase', 'handle':BodyChase(motion, redBallTracker)});
        self.naoBody_sm.addState({'name':'bodySearch', 'handle':BodySearch(motion, redBallTracker)});
        self.naoBody_sm.addState({'name':'bodyApproach', 'handle':BodyApproach(motion)});
        self.naoBody_sm.addState({'name':'bodyKick', 'handle':BodyKick(motion)});
                 
        self.naoBody_sm.addTransition('bodyIdle', 'timeout', 'bodySearch');
        
        self.naoBody_sm.addTransition('bodyChase', 'ballLost', 'bodySearch');
        self.naoBody_sm.addTransition('bodyChase', 'ballClose', 'bodyApproach');
        
        self.naoBody_sm.addTransition('bodySearch', 'ballFound', 'bodyChase');
        
        self.naoBody_sm.addTransition('bodyApproach', 'ballFar', 'bodyChase');
        self.naoBody_sm.addTransition('bodyApproach', 'timeout', 'bodyChase');
        self.naoBody_sm.addTransition('bodyApproach', 'ballLost', 'bodySearch');
        self.naoBody_sm.addTransition('bodyApproach', 'kick', 'bodyKick');

        self.naoBody_sm.addTransition('bodyKick', 'done', 'bodyChase');
        self.naoBody_sm.addTransition('bodyKick', 'timeout', 'bodyChase');

        
    def enter(self):
        self.naoBody_sm.enter();
    
    def update(self):
        self.naoBody_sm.update();
    
    def exit(self):
        self.naoBody_sm.exit();


class BodyIdle(state.State):
     
    def __init__(self, motion, posture):
        super(BodyIdle,self).__init__();
        self.motion = motion;
        self.posture = posture;
        self.timeout = 1.0;
        self.t0 = 0;
     
    def enter(self):
        print 'BodyIdle enter';
        self.motion.post.stiffnessInterpolation("Body", 1.0, 1.0);    
        self.motion.post.moveInit();
        
        proxyId = self.posture.post.goToPosture("StandInit", 1.0);
        self.motion.wait(proxyId, 0);

        self.t0 = time.time();
            
     
    def update(self):
        t = time.time();
        
        if (t - self.t0 > self.timeout):
            return 'timeout';
         
    def exit(self):
        print 'BodyIdle exit';


class BodyChase(state.State):
    threadTime = 0.2;
    fw_threshold = 0.5;
    bk_threshold = 0.3;
    retard = 1.0; #second
    maxTheta = 20*motion.TO_RAD;
    maxSpeedTheta = maxTheta/(21*0.02);
    stepPeriod = 21;
    stepFrequency = 1.0;
    minStepPeriod = 21;
    maxStepPeriod = 30;
     
    def __init__(self, motion, redBallTracker):
        super(BodyChase,self).__init__();
        self.motion = motion;
        self.redBallTracker = redBallTracker;
        self.threadTime = 0.2;
        self.countLost = 0;
        self.timeout = 3.0;

     
    def enter(self):
        print 'BodyChase enter';
        self.countLost = 0;
        self.firstRobotPositionTheta = self.motion.getRobotPosition(False);
     
    def update(self):
        if (self.redBallTracker.isNewData()):
            self.countLost = 0;
            targetPosition = self.redBallTracker.getPosition();
             
            # Compute target distance
            targetDistance = math.sqrt(math.pow(targetPosition[0], 2) + math.pow(targetPosition[1], 2));
            targetDistance = int(targetDistance/0.1) * 0.1;
            if (targetDistance > self.fw_threshold):
                x = 1.0;
            elif (targetDistance < self.bk_threshold):
                x = -1.0;
            else:
                self.motion.setWalkTargetVelocity(0.0, 0.0, 0.0, self.stepFrequency);
                return 'ballClose';
                 
            # Compute target angle
            targetAngle = math.atan2(targetPosition[1], targetPosition[0]);
            targetAngle = int(targetAngle/(0.5*motion.TO_RAD))*(0.5*motion.TO_RAD);
             
            # Compute theta velocity to send to the robot
            currentRobotPosition = self.motion.getRobotPosition(False);
            currentRobotVelocity = self.motion.getRobotVelocity();
 
            stepPeriod = self.maxStepPeriod - self.stepFrequency*(self.maxStepPeriod-self.minStepPeriod);
             
            # Compute Robot Position
            robotDeplacementTheta = currentRobotPosition[2] - self.firstRobotPositionTheta[2];
            # Compute robotPosition with retard second
            nextRobotTheta = currentRobotVelocity[2]*self.retard + robotDeplacementTheta
            errorTheta = targetAngle - nextRobotTheta;
            dTheta = 0.0
            maxSpeedTheta = self.maxTheta/(stepPeriod*0.02);
            if (errorTheta/(stepPeriod*0.02) > maxSpeedTheta*0.5):
                dTheta = maxSpeedTheta*0.5
            elif(errorTheta/(stepPeriod*0.02) < -maxSpeedTheta*0.5):
                dTheta = -maxSpeedTheta*0.5
            else:
                dTheta = errorTheta/(stepPeriod*0.02)
            theta = dTheta/maxSpeedTheta
 
            self.motion.setWalkTargetVelocity(x, 0.0, theta, self.stepFrequency);
        else:
            self.countLost = self.countLost + 1;
            if (self.countLost*self.threadTime > self.timeout):
                self.motion.setWalkTargetVelocity(0.0, 0.0, 0.0, self.stepFrequency);
                return 'ballLost';
            
    def exit(self):
        print 'BodyChase exit';
 


class BodySearch(state.State):
     
    def __init__(self, motion, redBallTracker):
        super(BodySearch,self).__init__();
        self.motion = motion;
        self.redBallTracker = redBallTracker;
        self.stepFrequency = 1.0;
        self.direction = 1.0;
        self.turnVelocity = 0.3;
     
    def enter(self):
        print 'BodySearch enter';
     
    def update(self):
        self.motion.setWalkTargetVelocity(0.0, 0.0, self.direction*self.turnVelocity, self.stepFrequency);
        
        if (self.redBallTracker.isNewData()):
            return 'ballFound';
         
    def exit(self):
        print 'BodySearch exit';
 


class BodyApproach(state.State):
     
    def __init__(self, motion):
        super(BodyApproach,self).__init__();
        self.motion = motion;
        self.timeout = 1.0;
        self.t0 = 0;
     
    def enter(self):
        print 'BodyApproach enter';
     
    def update(self):
        pass
         
    def exit(self):
        print 'BodyApproach exit';
 


class BodyKick(state.State):
     
    def __init__(self, motion):
        super(BodyKick,self).__init__();
        self.motion = motion;
        self.timeout = 1.0;
        self.t0 = 0;
     
    def enter(self):
        print 'BodyKick enter';
     
    def update(self):
        pass
         
    def exit(self):
        print 'BodyKick exit';
 
