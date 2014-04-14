# Program 3: moving two robots at the same time

import sys
import time
from naoqi import ALProxy



def seek(motionProxy, ball_location):
	motionProxy.moveTowards(ball_location)
