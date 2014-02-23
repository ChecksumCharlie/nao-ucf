'''
Created on Jan 6, 2014

@author: Sarah
'''

from naoqi import ALProxy
#from naoqi import ALModule

if __name__ == '__main__':
    robot_ID = 9559
    robot_IP = "127.0.0.1"
    motion = ALProxy("ALMotion", robot_IP, robot_ID)
    tts = ALProxy("ALTextToSpeech", robot_IP, robot_ID)
    ball = ALProxy("ALRedBallTracker", robot_IP, robot_ID)
    x  = ball.getPosition()[0]
    y  = ball.getPosition()[1]
    theta  = 0
    
    motion.setStiffnesses("Body",1.0)
    motion.moveTo(x, y, theta)
