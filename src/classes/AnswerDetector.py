import cv2 as cv
import numpy as np
from classes.Grid import Grid
import constants.answers as answer_list

class AnswerDetector():
    def __init__(self, **kwargs):
        self.save_thresh = None

    def _get_circlish(self, img):
        copy = img.copy()
        copy = cv.cvtColor(copy, cv.COLOR_BGR2GRAY)
        zeros_copy = np.zeros_like(copy)

        thresh = cv.adaptiveThreshold(copy, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 15, 3)
        self.save_thresh = thresh
        contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        contour_list = []
        for contour in contours:
            approx = cv.approxPolyDP(contour,0.01*cv.arcLength(contour,True),True)
            x, y, w, h = cv.boundingRect(contour)
            area = cv.contourArea(contour)
            if ((len(approx) > 8) & (area > 100) ):
                pixels = max(w, h)
                if pixels < 30:
                    contour_list.append(contour)
        
        points = []
        for cnt in contour_list:
            x, y, w, h = cv.boundingRect(cnt)
            cx = int(x+w/2)
            cy = int(y+h/2)
            points.append((cx, cy))
            cv.circle(zeros_copy, (cx, cy), 9, (255,0,0), 2)
        
        cv.imshow("circles", zeros_copy)

        return points
    
    def _get_blobs(self, img, display=False):
        copy = img.copy()
        copy = cv.cvtColor(copy, cv.COLOR_BGR2GRAY)

        params = cv.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 350
        detector = cv.SimpleBlobDetector_create(params)
        
        keypoints = detector.detect(copy)
        points = [(int(kpt.pt[0]), int(kpt.pt[1])) for kpt in keypoints]
        
        if display:
            copy = cv.drawKeypoints(copy, keypoints, None, (0, 255, 0), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            cv.imshow("drawn", copy)
        
        return points
    
    def _merge_cols(self, cols):
        ret_pts = []

        for col in cols:
            for pt in col:
                ret_pts.append(pt)

        return ret_pts
    

    def _answers(self, left_cols, right_cols, img):
        self._get_blobs(img)

        # left_bubbles = self._merge_cols(left_cols)
        # right_bubbles = self._merge_cols(right_cols)
    
    def _expected_amount(self, cols):
        if cols is None:
            return False

        count = 0
        for side in cols:
            for col in side:
                count += len(col)

        return count == 46

    def detect(self, img):
        points = self._get_circlish(img)
        grid = Grid(points)
        side_cols = grid.side_most(2, output_img=img)

        if self._expected_amount(side_cols):
            left_cols, right_cols = side_cols
            answers = self._answers(left_cols, right_cols, img)
            print(answers)