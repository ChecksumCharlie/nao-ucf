import sys
import time
from naoqi import ALProxy
from math import sin, cos, sqrt, pi
import cv2
import urllib2
import numpy as np
import Image

# Robot ip address and port
IP = "127.0.0.1"
PORT = 9559

motion = ALProxy("ALMotion", IP, PORT)
motion.setStiffnesses("Body", 1.0)


while True:
   

	camProxy = ALProxy("ALVideoDevice", IP, PORT)
	resolution = 2    # VGA
	colorSpace = 11   # RGB

	videoClient = camProxy.subscribe("python_client", resolution, colorSpace, 5)

	

	# Get a camera image.
	# image[6] contains the image data passed as an array of ASCII chars.
	naoImage = camProxy.getImageRemote(videoClient)



	camProxy.unsubscribe(videoClient)


	# Now we work with the image returned and save it as a PNG  using ImageDraw
	# package.

	# Get the image size and pixel array.
	imageWidth = naoImage[0]
	imageHeight = naoImage[1]
	array = naoImage[6]

	# Create a PIL Image from our pixel array.
	im = Image.fromstring("RGB", (imageWidth, imageHeight), array)

	# Save the image.
	im.save("camImage.png", "PNG")

	img = cv2.imread('camImage.png', 1)

	# Convert BGR to HSV
	img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

	# define range of blue color in HSV
	lower = np.array([0,50,50])
	upper = np.array([10,255,255])

	# Threshold the HSV image to get only blue color areas
	img = cv2.inRange(img, lower, upper)

	# Finding contours in the grayscale image
	ret,thresh = cv2.threshold(img,127,255,0)
	contours,hierarchy = cv2.findContours(thresh, 1, 2)
	cnt = contours[0]

	# The function cv2.moments() gives a dictionary of all moment values calculated
	M = cv2.moments(cnt)

	cx = int(M['m10']/M['m00'])
	cy = int(M['m01']/M['m00'])

	print cy

	if (cy>400):
		sys.exit(0)
	if (cx>350):
		motion.moveTo(0.2, 0, -0.2)
	elif (cx<350):
		motion.moveTo(0.2, 0, 0.2)
	else:
		motion.moveTo(0.2, 0, 0)

 


