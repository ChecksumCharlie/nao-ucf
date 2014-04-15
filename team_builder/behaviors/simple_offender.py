from __future__ import division
import sys
import time
import math
from multiprocessing import Process

from util import nao_robot as robot

debug = 0
degrees_full_screen_sweep = 60 #approx.

class LogicFor:
    def __init__(self, RobotGiven):
        self.player = RobotGiven

    def update(self):
    	self.RobotLegs.postureProxy.goToPosture( "StandInit", 0.5 )
    	
    	# get values
		RedBall = self.player.getRedBall()

		if ( debug ):
			print "Ball: ", RedBall
			print "Enemy: ", Enemy
			print "Goal: ", Goal

		# begin behavior 
		# ~ currently assumes ball is stationary
		time.sleep(0.3)

		# if ball not in sight, get ball in sight s.t. we face the general dir of the ball
		while ( !in_sight( RedBall ) ):
			if ( vertical_RedBall_scan() ):
				break	
			rotate ( math.radians( degrees_full_screen_sweep ) )
			RedBall = self.player.getRedBall()
		
		# at this pt, robot sees the ball
		RedBall = self.player.getRedBall()
		bufferDist = 0.8 #TODO figure out the 'perfect' bufferDist
		goToBall( bufferDist , RedBall) 
		
		# find goal
		Goal = self.player.getYellowGoal()   # opponent's goal
		while ( !in_sight( Goal ) ):
			if ( vertical_Goal_scan() ):
				Goal = self.player.getYellowGoal()
				RedBall = self.player.getRedBall()
				while ( !(in_sight( RedBall ) && in_sight( Goal ) ) ):
					#TODO move back
					RedBall = self.player.getRedBall()
					Goal = self.player.getYellowGoal()
			else:
				walkSquareAroundBall( bufferDist )
				Goal = self.player.getYellowGoal()
				
		#move back until both goal posts are visible
		while ( len(Goal) < 4 ):
			#TODO move back
			Goal = self.player.getYellowGoal()
		
		# at this pt, robot sees ball and goal
    	RedBall = self.player.getRedBall()
		Goal = self.player.getYellowGoal()
		aim( RedBall, Goal )
		
		RedBall = self.player.getRedBall()
		goToBall( bufferDist, RedBall)
		
		#TODO line up feet for kicking
		#TODO kick
		
				
	# walk around ball while avoiding collision with ball with a maxAngle in radians
	def walkAroundBall ( self, dx, dy, bufferDist, maxAngle ):
		#do stuff
		
    # walks around the ball in a square until ball and goal are both in sight (ie in the same horizontal range)
    def walkSquareAroundBall ( self, bufferDist ):
    	#do stuff
                
    # returns true red ball is above or below current field of vision
    # ~assumes head pitch stays at value where red ball was found
    # if red ball not found at all it returns to the original head pitch and returns false
    def vertical_RedBall_scan ():
    	# some stuff
    
    # looks up for goal... returns true if goal is found
    def vertical_Goal_scan ():
    	#some stuff
    
    def in_sight( obj ):
    	return obj != []
                
	def goToBall(self, bufferDistance):
    	# some behavior
    
	# AIM: walk around ball until the ball is between goal posts
    def aim (self, RedBall, Goal):
		while ( !between_goal_posts ( RedBall, Goal ) ):
			#??...potentially calculate optimal movement angle &/or target location
			#TODO walkAroundBall ( ??...?? ):
			RedBall = self.player.getRedBall()
			Goal = self.player.getYellowGoal()
