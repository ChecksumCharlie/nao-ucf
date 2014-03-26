'''
Created on Jan 6, 2014

@author: Sarah
'''
import math
import time
from naoqi import ALProxy
    
# returns the distance between points a and b
def distance(a, b):
    return math.sqrt(math.pow(a,2)+math.pow(b,2))

# returns the slope between points a and b
def get_slope(a, b):
    return (b[1]-a[1])/(b[0]-a[0])

#returns the [x,y] of the desired location for the calculated spot for kicking
def get_target_loc(ball_loc, goal_loc, dist):
    target_loc = ball_loc
    if ball_loc[1]==0:
        target_loc[0] -= dist
    else:
        L1 = goal_loc[0]-ball_loc[0]
        L2 = goal_loc[1]-ball_loc[1]
        L3 = distance(L1,L2)
        x = dist*L1/L3
        y = dist*L2/L3
        target_loc[0]-=x
        target_loc[1]-=y
    return target_loc

# prints string str followed by the coordinates [x,y] of loc
def print_coordinates(str,loc):
    str = str,loc[0],loc[1]
    print str
    
if __name__ == '__main__':
    robot_ID = 9560
    robot_IP = "127.0.0.1"
    motion = ALProxy("ALMotion", "127.0.0.1", robot_ID)
    motion.setStiffnesses("Body",1.0)
    
    # get robot coordinates
    x = 3.55122# value taken from the translation coordinate for x on webots
    y = 0.321583 # y is actually z in the translaion of the robot on webots
    r1_loc = [x,y]
    print_coordinates("Robot 1's Location is: ",r1_loc)
    
    #set robot posture to prepare for walking - increased stability
    postureProxy = ALProxy("ALRobotPosture", robot_IP, robot_ID)
    postureProxy.goToPosture("StandInit", 0.5)

    #get ball coordinates
    ball = ALProxy("ALRedBallTracker", robot_IP, robot_ID)
    ball.startTracker()
    time.sleep(1)
    ball_loc = ball.getPosition()
    ball.stopTracker()
    print_coordinates('Ball Location is: ',ball_loc)
    
    #get goal location: hard-coded for now
    goal_loc = [4.5,0.0]
    print_coordinates("Goal Location is: ", goal_loc)
    
    '''go to the ball
    call chasing module here... hard-coded to start close enough to the ball for now
    ***ENDS GETTING TO BALL*****'''
    
    
    # get Robot's target location
    
    #buffer_dist = min dist away from ball robot must be to have room to re-orient itself to face towards the goal
    #0.1456m is the default step distance calculated based on:
    # X_step default dist = 0.04m
    # Y_step default dist = 0.14m
    # Z (overall step dist) = distance_formula(X_step,Y_step) = 0.1456m
    # info found at https://community.aldebaran-robotics.com/doc/1-14/naoqi/motion/control-walk.html#control-walk
    #I use 0.165 to allow a little extra room
    ball_loc[0] = 3.27022
    ball_loc[1] = -0.184492
    print_coordinates('Ball Location is: ',ball_loc)
    buffer_dist = 0.165 #probably will need to play with this value
    target_loc = get_target_loc(ball_loc, goal_loc, buffer_dist) #very temporary way of considering target_loc
    print_coordinates('Target Location is: ',target_loc)
    
    # **assumes robot is facing towards goal
    ball_loc[0] = 3.27022
    ball_loc[1] = -0.184492
    print_coordinates('Ball Location is: ',ball_loc)
    
    # get robot on the correct side of the ball without colliding with the ball
    step_dist_buffer = 0.3
    if r1_loc[0]>ball_loc[0]: # robot is between ball and goal (on wrong side of ball; x_direction)
        print 'robot is in front of ball'
        diff_y = r1_loc[1]-ball_loc[1]
        if diff_y<=0 and r1_loc[1]>ball_loc[1]-step_dist_buffer: # robot is to left of ball but not enough to avoid collision
            print 'robot is to the left of the ball but not by a safe amount'
            motion.moveTo(0, ball_loc[1]-step_dist_buffer-diff_y,0) # move more left to avoid collision
            print 'moved more left so now safe'
        elif diff_y>0 and r1_loc[1]<ball_loc[1]+step_dist_buffer: #robot is to right of ball but not enough to avoid collision
            print 'robot is right not enough'
            motion.moveTo(0, diff_y+step_dist_buffer, 0) # move more right to avoid collision
            print 'move robot right safe amount now yay'
        # **might need to re-orient towards goal to get right movement
        motion.moveTo((r1_loc[0]-ball_loc[0])-step_dist_buffer, 0, 0) #move x direction to get behind ball
    
    #print 'behind ball'
    # now is safe to move to target location without ball collision
    # **again, might need to re-orient towards goal to get right movement
    '''find out adjust amount, not target location'''
    
    x_adjust = r1_loc[0]-target_loc[0]
    y_adjust = r1_loc[1]-target_loc[1]
    if r1_loc[0]>=target_loc[0]:
        if r1_loc[1]>=target_loc[1]:
            motion.moveTo(x_adjust,y_adjust,0)   # move there   
        else:
            motion.moveTo(x_adjust,0-y_adjust,0)
    else:
        if r1_loc[1]>=target_loc[1]:
            motion.moveTo(0-x_adjust,y_adjust,0)   # move there   
        else:
            motion.moveTo(0-x_adjust,0-y_adjust,0)
            
    # update robot position
    r1_loc = motion.getPosition("LLeg",2, True)
    print_coordinates("Robot 1's Location is: ",r1_loc)
    
    # ** re-orient robot to face towards goal_loc to aim for kick.... also put robot in standinit position for stability when entering kicking module