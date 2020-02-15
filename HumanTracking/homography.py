import numpy as np
import cv2 as cv


def calc_homograph():
    pts_src = np.array([[306, 365], [933, 386], [830, 570], [335, 560]])
    pts_dst = np.array([[5, 325], [5, 5], [205, 85], [205, 250]])
    homograph, status = cv.findHomography(pts_src, pts_dst)
    return homograph
