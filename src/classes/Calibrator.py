import cv2 as cv
import numpy as np
import os
import json
from util.capture import capture

class Calibrator():
    def __init__(self, **kwargs):
        self.CYCLE_CAPTURES = kwargs['cycle_captures']
        self.GRID = kwargs['grid']
        self.INPUT_DIR = kwargs['input_dir']
        self.SAVE_DIR = kwargs['save_dir']
        self.CRITERIA = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        self.searching = False
        
        Calibrator.dist_dir = kwargs['save_dir']

    def _per_frame(self, src, copy, key_is):
        cv.imshow('src', src)
        
        if key_is('f'):
            self.searching = True
        
        if self.searching == True:
            gray = cv.cvtColor(copy, cv.COLOR_BGR2GRAY)
            ret, _ = cv.findChessboardCorners(gray, self.GRID, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)

            if ret:
                num_files = str(len(os.listdir(self.INPUT_DIR)))
                cv.imwrite(f"{self.INPUT_DIR}{num_files}.jpg", src)

                self.searching = False

    def capture_inputs(self):
        capture(self._per_frame)

    def calibrate(self):
        objpoints = []
        imgpoints = []
        objp = np.zeros((1, self.GRID[0]*self.GRID[1], 3), np.float32)
        objp[0,:,:2] = np.mgrid[0:self.GRID[0], 0:self.GRID[1]].T.reshape(-1,2)

        fnames = os.listdir(self.INPUT_DIR)
        for name in fnames:
            img = cv.imread(self.INPUT_DIR + name)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            ret, corners = cv.findChessboardCorners(gray, self.GRID, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)

            if ret == True:
                objpoints.append(objp)
                pixel_corners = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), self.CRITERIA)
                imgpoints.append(pixel_corners)

                if self.CYCLE_CAPTURES:
                    img = cv.drawChessboardCorners(img, self.GRID, pixel_corners, True)
                    cv.imshow("img", img)
                    cv.waitKey(0)

        size = cv.imread(self.INPUT_DIR + "0.jpg", cv.IMREAD_GRAYSCALE).shape[::-1]
        ret, mtx, dist, _, _ = cv.calibrateCamera(objpoints, imgpoints, size, None, None)
        toJSON = {
            "camera_matrix": mtx.tolist(),
            "distortion_coefficients": dist.tolist()
        }

        with open(self.SAVE_DIR, "w") as f:
            json.dump(toJSON, f, indent=4)