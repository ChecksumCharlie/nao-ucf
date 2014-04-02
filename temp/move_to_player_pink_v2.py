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
PORT = 9560



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
	lower_blue = np.array([110,50,50])
	upper_blue = np.array([130,255,255])

	# Threshold the HSV image to get only blue colors
	mask = cv2.inRange(img, lower_blue, upper_blue)

	# Bitwise-AND mask and original image
	img = cv2.bitwise_and(img,img, mask= mask)

	img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
	img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

	ret,thresh = cv2.threshold(img,127,255,0)
	contours,hierarchy = cv2.findContours(thresh, 1, 2)


	cnt = contours[0]
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

 


