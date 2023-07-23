import cv2 as cv
import numpy as np
import math
from classes.Grid import Grid

class AnswerDetector():
    def __init__(self, **kwargs):
        self.grid = Grid()

    def _get_circles(self, img):
        copy = img.copy()
        copy = cv.cvtColor(copy, cv.COLOR_BGR2GRAY)
        zeros_copy = np.zeros_like(copy)

        thresh = cv.adaptiveThreshold(copy, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 15, 3)
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

    def detect(self, img):
        points = self._get_circles(img)
        srt_pts = sorted(points, key=lambda  pt: pt[1])
        grid = []
            

        new_col = True
        for x1, y1 in srt_pts: # current point
            

            for col in grid:
                x2, y2 = col[-1] # most recent point in column.
                if abs(x2 - x1) < 15 and abs(y2 - y1) < 40:
                    col.append((x1, y1))
                    new_col = True
                    break
            if new_col == True:
                new_col = False
                grid.append([(x1, y1)])
    

        for col in grid:
            copy = img.copy()
            for pt in col:
                cv.circle(copy, (pt[0], pt[1]), 9, (255,0,255), 2)
            cv.imshow("img", copy)
            cv.waitKey(0)    

            cv.circle(img, (pt[0], pt[1]), 9, (255,0,255), 2)
            cv.imshow("img", img)
            cv.waitKey(0)