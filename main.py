"""
Author: Kushashwa Ravi Shrimali
"""

import cv2
import sys # Arg Parsing, the easy way
import numpy as np
from utils import BGR2BGRA
from utils import *


class Image:
    """
    Image Class
    ------------
    Parameters
    :img_path: (default=None), type: str
    -----------
    Methods
    * __len__(): args: None, returns: shape of the image
    * __str__(): args: None, returns: description of the image
    * __doc__(): args: None, returns: documentation of the class
    * roi_selector(): args: None, returns roi object
    * hull(): args: None, returns: hull array
    * face_detect(): args: None, returns: faces array
    * choose(): args: None, returns: chosen faces array
    * blur(): args: kernel_size=5, returns: portrait bokeh output image
    """
    def __init__(self, img_path=None):
        """
        :param img_path: str, image path, default = None
        """
        if img_path is None:
            print("img_path not mentioned")
        self.path = img_path
        self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        self.img_alpha = cv2.cvtColor(self.img, cv2.COLOR_RGB2RGBA)

        # For face detection
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.gray = None

    def __doc__(self):
        """
        Returns documentation of the class usage
        :return: str object (documentation)
        """
        usage = "Usage: img_object = Image(img_path='sample.png')"
        return usage

    def __len__(self):
        """
        :return: int, number of pixels in self.img object
        """
        return self.img.shape[0] * self.img.shape[1] * self.img.shape[2]
    
    def __str__(self):
        """
        :return: str, shape of the image in format of width - height - channels
        """
        shape = self.img.shape
        desc = "Image Shape: Width:  " + str(shape[0]) + " Height: " + str(shape[1]) + ", Channels: " + str(shape[2])
        return desc
    
    def roi_selector(self):
        """
        :return: roi object
        """
        # Convert to Gray Scale
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        roi = cv2.selectROI(self.gray)
        return roi
    
    def hull(self):
        """
        :return: list, list with hull points
        """
        ret, thresh = cv2.threshold(self.gray, 200, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        hull = []
        for i in range(len(contours)):
            hull.append(cv2.convexHull(contours[i], False))
        return hull

    def face_detect(self):
        """
        :return: list, faces detected (points)
        """
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(self.gray, 1.3, 5)
        return faces
    
    def choose(self, rois):
        num_rois = len(rois)
        final_rois = []

        for i in range(num_rois):
            print("Do you want this face? Y/N")
            this_roi = rois[i]
            temp = self.gray[int(this_roi[1]):int(this_roi[1] + this_roi[3]), int(this_roi[0]):int(this_roi[0] + this_roi[2])]
            cv2.imshow("Face: " + str(i+1), temp)
            k = cv2.waitKey(0)
            if ord("Y") == k or ord("y") == k:
                final_rois.append(this_roi)
                cv2.destroyAllWindows()
        return final_rois

    def blur(self, kernel_size=5):
        """
        :param kernel_size: int, kernel size for cv2.GaussianBlur
        :return: image, portrait-bokeh image
        """
        # Select ROI
        # roi = self.roi_selector()
        rois = self.face_detect()
        rois = self.choose(rois)
        img_cropped = generate_mask(self.img_alpha, rois)
        blur_image = cv2.GaussianBlur(self.img_alpha, (5, 5), 0)
        res = overlap(img_cropped, blur_image)
        return res


img_obj = Image(sys.argv[1])
portrait_bokeh_image = img_obj.blur()
print("BLUR SHAPE: ", portrait_bokeh_image.shape)
cv2.imwrite("blur.png", portrait_bokeh_image)

cv2.imshow("Input Image", img_obj.img)
cv2.imshow("Portrait Bokeh Output", portrait_bokeh_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
