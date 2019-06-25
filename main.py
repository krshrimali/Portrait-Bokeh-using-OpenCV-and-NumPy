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
    :alpha: (default=100), type: int
    -----------
    Methods
    * __len__(): args: None, returns: shape of the image
    * __str__(): args: None, returns: description of the image
    """
    def __doc__(self):
        usage = "Usage: img_object = Image(img_path='sample.png')"
        return usage

    def __init__(self, img_path=None, alpha=100):
        """
        Usage: img_object = Image(img_path='sample.png')
        """
        if img_path is None:
            return "img_path not mentioned"
        self.path = img_path
        self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        # alpha_image = BGR2BGRA(self.img, alpha)
        alpha_image = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.img_alpha = cv2.cvtColor(self.img, cv2.COLOR_RGB2RGBA)
        # For face detection
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        self.gray = None

    def __len__(self):
        return self.img.shape[0] * self.img.shape[1] * self.img.shape[2]
    
    def __str__(self):
        shape = self.img.shape
        desc = "Image Shape: Width:  " + str(shape[0]) + " Height: " + \
                str(shape[1]) + ", Channels: " + str(shape[2])
        return desc
    
    def roi_selector(self):
        # Convert to Gray Scale
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        roi = cv2.selectROI(self.gray)
        return roi
    
    def hull(self):
        ret, thresh = cv2.threshold(self.gray, 200, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, \
                cv2.CHAIN_APPROX_SIMPLE)

        hull = []
        for i in range(len(contours)):
            hull.append(cv2.convexHull(contours[i], False))
    
    def face_detect(self): 
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(self.gray, 1.3, 5)
        return faces
    
    def choose(self, rois):
        num_rois = len(rois)
        final_rois = []

        for i in range(num_rois):
            print("Do you want this face? Y/N")
            this_roi = rois[i]
            temp = self.gray[int(this_roi[1]):int(this_roi[1] + this_roi[3]), \
                    int(this_roi[0]):int(this_roi[0] + this_roi[2])]
            cv2.imshow("Face: " + str(i+1), temp)
            k = cv2.waitKey(0)
            if(ord("Y") == k or ord("y") == k):
                final_rois.append(this_roi)
                cv2.destroyAllWindows()
        return final_rois

    def blur(self):
        # Select ROI
        # roi = self.roi_selector()
        rois = self.face_detect()
        rois = self.choose(rois)
        img_cropped = generate_mask(self.img_alpha, rois)
             
        # croppedImage = self.gray[int(roi[1]):int(roi[1] + roi[3]), \
        #        int(roi[0]):int(roi[0] + roi[2])]
        blur = cv2.GaussianBlur(self.img_alpha, (5, 5), 0)
        res = overlap(img_cropped, blur)
        return res
        '''
        empty = np.ones(self.gray.shape, self.gray.dtype)

        empty[int(roi[1]):int(roi[1] + roi[3]), \
                int(roi[0]):int(roi[0] + roi[2])] = blur
        
        gray_copy = self.gray
        
        gray_copy[int(roi[1]):int(roi[1] + roi[3]), \
                int(roi[0]):int(roi[0] + roi[2])] = blur
        
        # res = cv2.bitwise_and(gray_copy, gray_copy, mask = empty)
        res = gray_copy
        return res
        # return res 
        '''


img_obj = Image(sys.argv[1], alpha=0)
print(img_obj)
print(len(img_obj))
# TODO: img_obj = Image() should return an error
blur = img_obj.blur()
print("BLUR SHAPE: ", blur.shape)
cv2.imwrite("blur.png", blur)

cv2.imshow("Blur", blur)
cv2.waitKey(0)
cv2.destroyAllWindows()
