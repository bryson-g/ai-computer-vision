import cv2 as cv
import numpy as np
import json
from classes.Calibrator import Calibrator
from util.capture import capture

class ParlayScanner:
    def __init__(self, **kwargs):
        self.test_scene = kwargs['test_scene']
        self.dist_dir = kwargs['dist_dir']

        if self.test_scene is None:
            capture(self.per_frame)
        else:
            src = cv.imread(self.test_scene)
            self.per_frame(src, src.copy(), lambda x: print("nope"))

    def _undistort(self, img):
        with open(self.dist_dir, 'r') as f:
            dist_data = json.load(f)
        mtx = np.array(dist_data["camera_matrix"])
        dist = np.array(dist_data["distortion_coefficients"])

        h,w = img.shape[:2]
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
        dst = cv.undistort(img, mtx, dist, None, newcameramtx)
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]

        return dst


    def per_frame(self, src, copy, key_is):
        cv.imshow("src", src)
        dst = self._undistort(src)
        cv.imshow("dst", dst)

        if self.test_scene is not None:
            cv.waitKey(0)