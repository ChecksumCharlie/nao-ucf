'''
Created on Nov 9, 2013

@author: Astrid
'''

import time;
import math;

from util import state_machine;
from util import state;

class NaoHead(object):
    naoHead_sm = None;

    def __init__(self, motion, redBallTracker):
        self.naoHead_sm = state_machine.StateMachine({'name':'headIdle', 'handle': HeadIdle(motion)});
        self.naoHead_sm.addState({'name':'headScan', 'handle':HeadScan(motion, redBallTracker)});
        self.naoHead_sm.addState({'name':'headTrack', 'handle':HeadTrack(motion, redBallTracker)});
         
        self.naoHead_sm.addTransition('headIdle', 'timeout', 'headTrack');
        self.naoHead_sm.addTransition('headTrack', 'ballLost', 'headScan');
        self.naoHead_sm.addTransition('headScan', 'ballFound', 'headTrack');
        
    def enter(self):
        self.naoHead_sm.enter();
    
    def update(self):
        self.naoHead_sm.update();
    
    def exit(self):
        self.naoHead_sm.exit();
        

class HeadIdle(state.State):
     
    def __init__(self, motion):
        super(HeadIdle,self).__init__();
        self.timeout = 1.0;
        self.t0 = 0;
        self.motion = motion;
     
    def enter(self):
        print 'HeadIdle enter';
        self.t0 = time.time();
        
        yaw = 0;
        pitch = -15*math.pi/180;
        
        names = ["HeadYaw", "HeadPitch"];
        angles = [yaw, pitch];
        fractionMaxSpeed = 0.2
                  
        self.motion.setStiffnesses("Head", 1.0);
        self.motion.post.setAngles(names, angles, fractionMaxSpeed);
        self.motion.setStiffnesses("Head", 0.0);
     
    def update(self):
        t = time.time();
        
        if (t - self.t0 > self.timeout):
            return 'timeout';
         
    def exit(self):
        print 'HeadIdle exit';
 
 
class HeadTrack(state.State):
     
    def __init__(self, motion, redBallTracker):
        super(HeadTrack,self).__init__();
        self.motion = motion;
        self.redBallTracker = redBallTracker;
        self.threadTime = 0.2;
        self.countLost = 0;
        self.timeout = 1.0;
        
    def enter(self):
        print 'HeadTrack enter';
        self.countLost = 0;
                 
        self.motion.setStiffnesses("Head", 1.0);
        self.redBallTracker.startTracker();

     
    def update(self):
        if (self.redBallTracker.isNewData()):
            self.countLost = 0;
        else:
            self.countLost = self.countLost + 1;
            if (self.countLost*self.threadTime > self.timeout):
                return 'ballLost';
         
    def exit(self):
        print 'HeadTrack exit';
        self.redBallTracker.stopTracker();
 
 
class HeadScan(state.State):
     
    def __init__(self, motion, redBallTracker):
        super(HeadScan,self).__init__();
        self.motion = motion;
        self.redBallTracker = redBallTracker;
     
    def enter(self):
        print 'HeadScan enter';
        self.scanTime = 3.0;
        self.direction = 1.0;
        
        self.t0 = time.time();
        
        # start scan in ball's last known position
        
        self.motion.setStiffnesses("Head", 1.0);
        self.redBallTracker.startTracker();
     
    def update(self):
        t = time.time();
        
        if (self.redBallTracker.isNewData()):
            print "Ball detected";
            return 'ballFound';
        
        # update head position: continuously scanning left-right and up-down
        ph = 2*math.pi*(t-self.t0)/self.scanTime;
        yaw = 60*math.pi/180*self.direction*math.asin(math.sin(ph));
        pitch = 30*math.pi/180 + 20*math.pi/180*math.cos(ph);

        names = ["HeadYaw", "HeadPitch"];
        angles = [yaw, pitch];
        fractionMaxSpeed = 0.2;

        self.motion.setAngles(names, angles, fractionMaxSpeed);
         
    def exit(self):
        print 'HeadScan exit';
        self.redBallTracker.stopTracker();

        