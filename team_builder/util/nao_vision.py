
from naoqi import ALProxy
from math import sin, cos, sqrt, pi
import cv2
import numpy as np
import Image
import time


class RobotEyes:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT

        self.timerTopCam = time.time()
        self.timerBottomCam = time.time()

        # Parameters for Camera Proxy
        self.camProxy = ALProxy("ALVideoDevice", self.IP, self.PORT)
        self.resolution = 2    # VGA
        self.colorSpace = 11   # RGB
        self.bottomCam = 1
        self.topCam = 0

        ## add conditionals
        # self.camProxy.unsubscribe("python_client")
        # self.camProxy.unsubscribe("python_client_2")


        # Subscribe to Camera Proxy
        self.videoClient = self.camProxy.subscribeCamera("python_client", self.topCam, self.resolution, self.colorSpace, 5)
        self.videoClient2 = self.camProxy.subscribeCamera("python_client", self.bottomCam, self.resolution, self.colorSpace, 5)
        self.naoImageTop = self.camProxy.getImageRemote(self.videoClient)
        self.naoImageBottom = self.camProxy.getImageRemote(self.videoClient2)

    def __del__(self):
        # Unsubsribe from Camera Proxy
        self.camProxy.unsubscribe(self.videoClient)
        self.camProxy.unsubscribe(self.videoClient2)

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

        # # Convert BGR to HSV
        # self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

        # # define range of blue color in HSV
        # # Blue Belt
        # self.lower = np.array([0,50,50])
        # self.upper = np.array([10,255,255])


        # # Threshold the HSV image to get only blue color areas
        # self.img = cv2.inRange(self.img, self.lower, self.upper)

        cv2.imshow('image',self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def getImageHSV(self):
        # Get a camera image.
        # image[6] contains the image data passed as an array of ASCII chars.
        if (time.time() - self.timerTopCam > 1):
            self.naoImageTop = self.camProxy.getImageRemote(self.videoClient)
            self.timerTopCam = time.time()
        

        # Get the image size and pixel array.
        imageWidth = self.naoImageTop[0]
        imageHeight = self.naoImageTop[1]
        array = self.naoImageTop[6]

        # Create a PIL Image from our pixel array.
        im = Image.fromstring("RGB", (imageWidth, imageHeight), array)

        # Create a BGR Numpy pixel array from  camera image
        img = np.array(im)

        # Convert BGR to HSV
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        return img

    def getImage2HSV(self):
        # Get a camera image.
        # image[6] contains the image data passed as an array of ASCII chars.
        if (time.time() - self.timerBottomCam > 1):
            self.naoImageBottom = self.camProxy.getImageRemote(self.videoClient2)
            timerBottomCam = time.time()
            

        # Get the image size and pixel array.
        imageWidth = self.naoImageBottom[0]
        imageHeight = self.naoImageBottom[1]
        array = self.naoImageBottom[6]

        # Create a PIL Image from our pixel array.
        im = Image.fromstring("RGB", (imageWidth, imageHeight), array)

        # Create a BGR Numpy pixel array from  camera image
        img = np.array(im)

        # Convert BGR to HSV
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        return img

    def getCoordsGivenThresh(self, img, lower, upper):
         # Threshold the HSV image to get only blue color areas
        img = cv2.inRange(img, lower, upper)

        # Finding contours in the grayscale image
        ret,thresh = cv2.threshold(img,127,255,0)
        contours,hierarchy = cv2.findContours(thresh, 1, 2)

        coords = []

        for c in contours:

            # The function cv2.moments() gives a dictionary of all moment values calculated
            M = cv2.moments(c)

            # m00 - contour area
            # m10 - sum of all points distance to x-axis
            # m01 - sum of all points distance to y-axis
            # ==> centroid_x = M10/M00 and centroid_y = M01/M00
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            coords += [cx, cy]

        return coords

    def getSingleCoordGivenThresh(self, img, lower, upper):
         # Threshold the HSV image to get only blue color areas
        img = cv2.inRange(img, lower, upper)

        # Finding contours in the grayscale image
        ret,thresh = cv2.threshold(img,127,255,0)
        contours,hierarchy = cv2.findContours(thresh, 1, 2)

        # starting values for an all encompassing bounding rectangle diagonal point pair
        # anything detected on screen will be a smaller/higher value respectively (min/max)
        x_min = 640
        y_min = 480
        x_max = 0
        y_max = 0

        for c in contours:

            # get the bounding rectangle for each individual shape detected
            x,y, w, h = cv2.boundingRect(c)
    
            # keep the min and max values of each
            if (x<=x_min): x_min = x
            if (y<=y_min): y_min = y
            if (x+w>=x_max): x_max = x+w
            if (y+h>=y_max): y_max = y+h
           
        # after loop, calculate the mid point of the all-bounding rectangle
        rect_mid_x = (x_max-x_min)/2+x_min
        rect_mid_y = (y_max-y_min)/2+y_min
        
        coords = [rect_mid_x, rect_mid_y]

        # return [] if nothing has been detected meaning starting values are the same
        if (x_min == 640 and y_min == 480 and x_max == 0 and y_max == 0):
            coords = []

        return coords

    def getHeightGivenColorThresh(self, img, lower, upper):
           # Threshold the HSV image to get only blue color areas
        img = cv2.inRange(img, lower, upper)

        # Finding contours in the grayscale image
        ret,thresh = cv2.threshold(img,127,255,0)
        contours,hierarchy = cv2.findContours(thresh, 1, 2)

        # starting values for an all encompassing bounding rectangle diagonal point pair
        # anything detected on screen will be a smaller/higher value respectively (min/max)
        x_min = 640
        y_min = 480
        x_max = 0
        y_max = 0

        for c in contours:

            # get the bounding rectangle for each individual shape detected
            x,y, w, h = cv2.boundingRect(c)
    
            # keep the min and max values of each
            if (x<=x_min): x_min = x
            if (y<=y_min): y_min = y
            if (x+w>=x_max): x_max = x+w
            if (y+h>=y_max): y_max = y+h
           
        # after loop, calculate the mid point of the all-bounding rectangle
        rect_h = (x_max-x_min)/2+x_min
        
        
        height = y_max - y_min

        # return [] if nothing has been detected meaning starting values are the same
        if (x_min == 640 and y_min == 480 and x_max == 0 and y_max == 0):
            height = None

        return height

    def getWidthGivenColorThresh(self, img, lower, upper):
        # Threshold the HSV image to get only blue color areas
        img = cv2.inRange(img, lower, upper)

        # Finding contours in the grayscale image
        ret,thresh = cv2.threshold(img,127,255,0)
        contours,hierarchy = cv2.findContours(thresh, 1, 2)

        # starting values for an all encompassing bounding rectangle diagonal point pair
        # anything detected on screen will be a smaller/higher value respectively (min/max)
        x_min = 640
        y_min = 480
        x_max = 0
        y_max = 0

        for c in contours:

            # get the bounding rectangle for each individual shape detected
            x,y, w, h = cv2.boundingRect(c)
    
            # keep the min and max values of each
            if (x<=x_min): x_min = x
            if (y<=y_min): y_min = y
            if (x+w>=x_max): x_max = x+w
            if (y+h>=y_max): y_max = y+h
           
        # after loop, calculate the mid point of the all-bounding rectangle
        rect_h = (x_max-x_min)/2+x_min
        
        
        width = x_max - x_min

        # return [] if nothing has been detected meaning starting values are the same
        if (x_min == 640 and y_min == 480 and x_max == 0 and y_max == 0):
            width = None

        return width

    def getRedBall(self):
        # Red Ball
        lower = np.array([110,150,150])
        upper = np.array([130,255,255])

        img = self.getImageHSV()
        
        return self.getCoordsGivenThresh(img, lower, upper)

    def getBlueGoal(self):
        # Blue Goal
        lower = np.array([10,50,50])
        upper = np.array([20,255,255])

        img = self.getImageHSV()

        return self.getSingleCoordGivenThresh(img, lower, upper)

    def getYellowGoal(self):
        # Yellow Goal
        lower = np.array([85,100,100])
        upper = np.array([105,255,255])

        img = self.getImageHSV()
        
        return self.getSingleCoordGivenThresh(img, lower, upper)

    def getBluePlayers(self):
        # Blue Belt
        lower= np.array([0,50,50])
        upper = np.array([10,255,255])

        img = self.getImageHSV()

        return self.getCoordsGivenThresh(img, lower, upper)

    def getPinkPlayers(self):
        # Pink Belt
        lower = np.array([110,50,50])
        upper = np.array([130,150,255])

        img = self.getImageHSV()
        
        return self.getCoordsGivenThresh(img, lower, upper)


    def getRedBall2(self):
        # Red Ball
        lower = np.array([110,150,150])
        upper = np.array([130,255,255])

        img = self.getImage2HSV()

        return self.getCoordsGivenThresh(img, lower, upper)

    def getBlueGoal2(self):
        # Blue Goal
        lower = np.array([10,50,50])
        upper = np.array([20,255,255])

        img = self.getImage2HSV()

        return self.getSingleCoordGivenThresh(img, lower, upper)

    def getYellowGoal2(self):
        # Yellow Goal
        lower = np.array([85,100,100])
        upper = np.array([105,255,255])

        img = self.getImage2HSV()
        
        return self.getSingleCoordGivenThresh(img, lower, upper)

    def getBluePlayers2(self):
        # Blue Belt
        lower= np.array([0,50,50])
        upper = np.array([10,255,255])

        img = self.getImage2HSV()

        return self.getCoordsGivenThresh(img, lower, upper)

    def getPinkPlayers2(self):
        # Pink Belt
        lower = np.array([110,50,50])
        upper = np.array([130,150,255])

        img = self.getImage2HSV()
        
        return self.getCoordsGivenThresh(img, lower, upper)

    def getYellowGoalHeight(self):

        # Yellow Goal
        lower = np.array([85,100,100])
        upper = np.array([105,255,255])

        img = self.getImageHSV()
        
        return self.getHeightGivenColorThresh(img, lower, upper)

    def getBlueGoalHeight(self):
        # Blue Goal
        lower = np.array([10,50,50])
        upper = np.array([20,255,255])

        img = self.getImageHSV()

        return self.getHeightGivenColorThresh(img, lower, upper)

    def getYellowGoalWidth(self):

        # Yellow Goal
        lower = np.array([85,100,100])
        upper = np.array([105,255,255])

        img = self.getImageHSV()
        
        return self.getWidthGivenColorThresh(img, lower, upper)

    def getBlueGoalWidth(self):
        # Blue Goal
        lower = np.array([10,50,50])
        upper = np.array([20,255,255])

        img = self.getImageHSV()

        return self.getWidthGivenColorThresh(img, lower, upper)
       

        
