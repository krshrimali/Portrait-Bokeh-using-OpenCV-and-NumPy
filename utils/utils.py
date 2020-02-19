"""
Author: Kushashwa Ravi Shrimali
Utility File for Portrait Bokeh
"""

import cv2
import numpy as np


def BGR2BGRA(img, ones=True, alpha=255):
    """
    Apply BGR to BGRA conversion
    -----------
    Parameters
    :img: np.ndarray type
    :ones: (default=True) - to be removed #TODO
    :alpha: (default=100) - for transparency
    -----------
    Returns
    :img: np.ndarray type (4 channel image, save as png to visualize)
    """
    b, g, r = cv2.split(img)
    # making everything opaque?
    alpha_channel = np.ones(b.shape, dtype=b.dtype) * alpha
    img_BGRA = cv2.merge((b, g, r, alpha_channel))
    return img_BGRA


def circ_func(x, y, r, c):
    return (x - c[0])**2 + (y - c[1])**2 - r**2 > 0


def crop_circle(img, roi):
    """
    Crop Circle
    ------------
    Parameters:
    :img: np.ndarray type
    # /:roi: [(roi[1]:roi[1] + roi[3]), (roi[0]:roi[0] + roi[2])]
    :roi: [radius, center]
    -----------
    Returns
    :img: np.ndarray type (with cropped portion with alpha = 0.0 everything else 100.0)
    """
    radius = roi[0]
    center = roi[1]

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            is_outside = circ_func(j, i, r=radius, c=center)
            if(is_outside == False):
                img[i][j][3] = 255
            elif(img[i][j][3] != 255):
                img[i][j][3] = 0
    return img


def generate_mask(img, rois):
    # Initialize with transparency levels
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j][3] = 0
    i = 0
    for roi in rois:
        print(roi)
        roi = list(roi)
        if roi[2] != roi[3]:
            if roi[2] > roi[3]:
                roi[2] = roi[3]
            else:
                roi[3] = roi[2]
        list_ = [int(roi[2]/2.0), [roi[0] + int(roi[2]/2.0), roi[1] + int(roi[3]/2.0)]]
        if i == 0:
            img_cropped = crop_circle(img, list_)
        else:
            img_cropped = crop_circle(img_cropped, list_)
        cv2.imwrite("img_cropped_"+str(i)+".png", img_cropped)
        i+=1
    return img_cropped


def overlap(imgA, imgB):
    if imgA.shape != imgB.shape:
        print("Both should be 4 and equal")
        return -1

    img = np.zeros(imgA.shape, imgA.dtype)

    for i in range(imgA.shape[0]):
        for j in range(imgA.shape[1]):
            if imgA[i][j][3] == 255:
                img[i][j] = imgA[i][j]
            elif imgA[i][j][3] == 0:
                img[i][j] = imgB[i][j]
                img[i][j][3] = 255

    return img
