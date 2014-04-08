
from naoqi import ALProxy
from math import sin, cos, sqrt, pi
import cv2
import numpy as np
import Image


class RobotEyes:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT

        # Parameters for Camera Proxy
        self.camProxy = ALProxy("ALVideoDevice", self.IP, self.PORT)
        self.resolution = 2    # VGA
        self.colorSpace = 11   # RGB

        # Subscribe to Camera Proxy
        self.videoClient = self.camProxy.subscribe("python_client", self.resolution, self.colorSpace, 5)

        
    def __del__(self):
        # Unsubsribe from Camera Proxy
        self.camProxy.unsubscribe(self.videoClient)

    def displayImage(self):
        # Get a camera image.
        # image[6] contains the image data passed as an array of ASCII chars.
        self.naoImage = self.camProxy.getImageRemote(self.videoClient)

        # Get the image size and pixel array.
        self.imageWidth = self.naoImage[0]
        self.imageHeight = self.naoImage[1]
        self.array = self.naoImage[6]

        # Create a PIL Image from our pixel array.
        self.im = Image.fromstring("RGB", (self.imageWidth, self.imageHeight), self.array)

        # Create a BGR Numpy pixel array from  camera image
        self.img = np.array(self.im)

        # Convert BGR to HSV
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

        # define range of blue color in HSV
        # Blue Belt
        self.lower = np.array([0,50,50])
        self.upper = np.array([10,255,255])

        # Blue Goal
        self.lower = np.array([11,50,50])
        self.upper = np.array([28,202,187])

        # Pink Player
        self.lower = np.array([110,50,50])
        self.upper = np.array([130,255,255])

        # Orange Ball
        self.lower = np.array([100,50,50])
        self.upper = np.array([109,235,255])

        # Yellow Goal
        self.lower = np.array([75,50,50])
        self.upper = np.array([99,199,253])

        # Threshold the HSV image to get only blue color areas
        self.img = cv2.inRange(self.img, self.lower, self.upper)

        cv2.imshow('image',self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def getImageHSV(self):
        # Get a camera image.
        # image[6] contains the image data passed as an array of ASCII chars.
        naoImage = self.camProxy.getImageRemote(self.videoClient)

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

        return img

    def getMomentsGivenColorThresh(self, img, lower, upper):
         # Threshold the HSV image to get only blue color areas
        img = cv2.inRange(img, lower, upper)

        # Finding contours in the grayscale image
        ret,thresh = cv2.threshold(img,127,255,0)
        contours,hierarchy = cv2.findContours(thresh, 1, 2)

        if (len(contours) <= 0):
            return None
        else:
            cnt = contours[0]
            # The function cv2.moments() gives a dictionary of all moment values calculated
            M = cv2.moments(cnt)
            return M

    def calculateCentroidXY(self, moments):
            M = moments
            # m00 - contour area
            # m10 - sum of all points distance to x-axis
            # m01 - sum of all points distance to y-axis
            # ==> centroid_x = M10/M00 and centroid_y = M01/M00
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            return [cx, cy]

    def getOrangeBall(self):
        # Orange Ball
        lower = np.array([100,50,50])
        upper = np.array([109,235,255])

        img = self.getImageHSV()
        M = self.getMomentsGivenColorThresh(img, lower, upper)

        if (M == None):
            return None
        else:
            return self.calculateCentroidXY(M)

    def getBlueGoal(self):
        # Blue Goal
        self.lower = np.array([11,50,50])
        self.upper = np.array([28,202,187])

        img = self.getImageHSV()
        M = self.getMomentsGivenColorThresh(img, lower, upper)

        if (M == None):
            return None
        else:
            return self.calculateCentroidXY(M)

    def getYellowGoal(self):
        # Yellow Goal
        self.lower = np.array([75,50,50])
        self.upper = np.array([99,199,253])

        img = self.getImageHSV()
        M = self.getMomentsGivenColorThresh(img, lower, upper)

        if (M == None):
            return None
        else:
            return self.calculateCentroidXY(M)

       

        