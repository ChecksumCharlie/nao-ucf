from __future__ import division

import math
import time

debug = 0
degrees_full_screen_sweep = 60 #approx.

class LogicFor:
    def __init__(self, RobotGiven):
        self.player = RobotGiven
    
    
    def update(self):
        self.player.RobotLegs.postureProxy.goToPosture( "StandInit", 0.5 )
    
        # get values
        RedBall = self.player.getRedBall()
        if ( debug ):
            print "Ball: ", RedBall
        
        # begin behavior 
        # ~ currently assumes ball is stationary
        time.sleep(0.3)
        
        # if ball not in sight, get ball in sight s.t. we face the general dir of the ball
        while ( self.in_sight( RedBall ) == False ):
            if ( self.vertical_RedBall_scan() ):
                break	
            self.rotate ( math.radians( degrees_full_screen_sweep ) )
            RedBall = self.player.getRedBall()
        
        # at this pt, robot sees the ball
        RedBall = self.player.getRedBall()
        bufferDist = 0.8 #TODO figure out the 'perfect' bufferDist
        self.goToBall( bufferDist ) 
        
        # find goal
        Goal = self.player.getYellowGoal()   # opponent's goal
        while ( self.in_sight( Goal ) == False ):
            if ( self.vertical_Goal_scan() ):
                Goal = self.player.getYellowGoal()
                RedBall = self.player.getRedBall()
                while ( self.in_sight( RedBall ) == False and self.in_sight( Goal ) == False ):
                    #TODO move back
                    RedBall = self.player.getRedBall()
                    Goal = self.player.getYellowGoal()
            else:
                self.walkSquareAroundBall( bufferDist )
                Goal = self.player.getYellowGoal()
        '''
        # move back until both goal posts are visible
        while ( len(Goal) < 4 ):
            # TODO move back
            Goal = self.player.getYellowGoal()
        '''
        # at this pt, robot sees ball and goal
        RedBall = self.player.getRedBall()
        Goal = self.player.getYellowGoal()
        self.aim( RedBall, Goal )
        
        RedBall = self.player.getRedBall()
        self.goToBall( bufferDist, RedBall )
        
        # TODO line up feet for kicking
        # TODO kick
        
        # TODO Evaluate and Take on Role
    
    # returns true red ball is above or below current field of vision
    # ~assumes head pitch stays at value where red ball was found
    # if red ball not found at all it returns to the original head pitch and returns false
    def vertical_RedBall_scan ( self ):
        # some stuff
        None
    
    # looks up for goal... returns true if goal is found
    def vertical_Goal_scan ( self ):
        #some stuff
        None
    
    def walkAroundBall ( self, dx, dy, bufferDist, maxAngle ):
        #do stuff
        None
    
    # walks around the ball in a square until ball and goal are both in sight (ie in the same horizontal range)
    def walkSquareAroundBall ( self, bufferDist ):
        #do stuff
        None
    
    def in_sight( self, obj ):
        return obj != []
    
    def between_goal_posts ( self, RedBall, Goal ):
        return self.in_sight(Goal)
    
    def goToBall(self, bufferDistance):
        # some behavior
        None
    
    # AIM: walk around ball until the ball is between goal posts
    def aim (self, RedBall, Goal):
        while ( self.between_goal_posts( RedBall, Goal ) == False ):
            #??...potentially calculate optimal movement angle &/or target location
            #TODO walkAroundBall ( ??...?? ):
            RedBall = self.player.getRedBall()
            Goal = self.player.getYellowGoal()
    