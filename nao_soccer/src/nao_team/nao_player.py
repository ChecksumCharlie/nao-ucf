'''
Created on Nov 9, 2013

@author: Astrid
'''

import sys;

from naoqi import ALProxy;

import nao_head;
import nao_body;

class NaoPlayer(object):
    '''
    classdocs
    '''
    port = 9559;


    def __init__(self, robotIp, robotPort):
        self.ip = robotIp;
        self.port = robotPort;
#         self.playerId = playerId;
#         self.teamId = teamId;

        try:
            self.motion = ALProxy("ALMotion", self.ip, self.port);
        except Exception,e:
            print "Could not create proxy to ALMotion";
            print "Error was: ",e;
            sys.exit(1);

        try:
            self.posture = ALProxy("ALRobotPosture", self.ip, self.port);
        except Exception, e:
            print "Could not create proxy to ALRobotPosture";
            print "Error was: ", e;
        
        try:
            self.redBallTracker = ALProxy("ALRedBallTracker", self.ip, self.port);
        except Exception,e:
            print "Could not create proxy to ALRedBallTracker";
            print "Error was: ",e;
     
        self.naoBody = nao_body.NaoBody(self.motion, self.posture, self.redBallTracker);
        self.naoHead = nao_head.NaoHead(self.motion, self.redBallTracker);
        
        
    def enter(self):
        self.naoHead.enter();
        self.naoBody.enter();
    
    def update(self):
        self.naoHead.update();
        self.naoBody.update();
    
    def exit(self):
        self.naoHead.exit();
        self.naoBody.exit();
#         self.motion.stiffnessInterpolation("Body", 0.0, 1.0);     