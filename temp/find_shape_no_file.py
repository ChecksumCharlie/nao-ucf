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
PORT = 9563

# Parameters for Camera Proxy
camProxy = ALProxy("ALVideoDevice", IP, PORT)
resolution = 2    # VGA
colorSpace = 11   # RGB

# Subscribe to Camera Proxy
videoClient = camProxy.subscribe("python_client", resolution, colorSpace, 5)

# Get a camera image.
# image[6] contains the image data passed as an array of ASCII chars.
naoImage = camProxy.getImageRemote(videoClient)

# Unsubsribe from Camera Proxy
camProxy.unsubscribe(videoClient)

# Get the image size and pixel array.
imageWidth = naoImage[0]
imageHeight = naoImage[1]
array = naoImage[6]

# Create a PIL Image from our pixel array.
im = Image.fromstring("RGB", (imageWidth, imageHeight), array)

# Create a BGR Numpy pixel array from  camera image
img = np.array(im)

# Convert BGR to HSV
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
img2 = img



# Blue Belt
lower= np.array([0,50,50])
upper = np.array([10,255,255])

# # Blue Goal
# lower = np.array([10,50,50])
# upper = np.array([20,255,255])

# # Pink Belt
# lower = np.array([110,50,50])
# upper = np.array([130,150,255])

# # Yellow Goal
# lower = np.array([85,100,100])
# upper = np.array([105,255,255])

# # Red Ball
# lower = np.array([110,150,150])
# upper = np.array([130,255,255])

# Threshold the HSV image to get only blue color areas
img = cv2.inRange(img, lower, upper)
img2 = img
# Finding contours in the grayscale image
ret,thresh = cv2.threshold(img,127,255,0)
contours,hierarchy = cv2.findContours(thresh, 1, 2)

for c in contours:

    # The function cv2.moments() gives a dictionary of all moment values calculated
    M = cv2.moments(c)

    # m00 - contour area
    # m10 - sum of all points distance to x-axis
    # m01 - sum of all points distance to y-axis
    # ==> centroid_x = M10/M00 and centroid_y = M01/M00
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    print cx
    print cy
 
cv2.imshow('image',img2)
cv2.waitKey(0)
cv2.destroyAllWindows()

# green = np.uint8([[[203, 202, 187 ]]])
# hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
# print hsv_green
