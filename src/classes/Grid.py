import cv2 as cv
import numpy as np
from math import sqrt

class Grid():
    def __init__(self, points):
        self.srt_pts = sorted(points, key=lambda  pt: pt[1])
        self.srt_pts = self._filter_pts(self.srt_pts, cycle=False)
        self.grid = []
        self._create()
    
    def _create(self):
        for pt in self.srt_pts:
            found_col = self._find_pt_column(pt)
            if not found_col:
                self.grid.append([pt])

    def _filter_pts(self, points, cycle=False):
        filtered = []
        for pt1 in points:
            too_close = False

            for pt2 in filtered:
                distance = sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)
                if distance < 10:
                    too_close = True
                    break
            
            if too_close == False:
                filtered.append(pt1)
        return filtered



    def _find_pt_column(self, pt):
        currX, currY = pt
        for col in self.grid:
            lastX, lastY = col[-1]
            xDis = abs(currX - lastX)
            yDis = abs(currY - lastY)

            if xDis < 15 and yDis < 40:
                col.append(pt)
                return True
            
        return False
    
    def side_most(self, amount, output_img=None):
        # less than expected amount of cols.
        if len(self.grid) < amount * 2:
            return

        left_cols = []
        right_cols = []

        left_sorted = sorted(self.grid, key = lambda col: col[0][0])
        for i in range(amount):
            left_cols.append(left_sorted[i])
        
        right_sorted = left_sorted[::-1]
        for i in range(amount):
            right_cols.append(right_sorted[i])

        # DISPLAY #
        if output_img is not None:
            img = output_img.copy()
            for grid in left_cols + right_cols:
                for pt in grid:
                    cv.circle(img, (pt[0], pt[1]), 7, (0,255,0), 2)
            cv.imshow("grid_side_most_img", img)
        
        return (left_cols, right_cols)
    
    def display(self, img, cycle=False):
        img = img.copy()
        for col in self.grid:
            anchor = col[0]
            for pt in col:
                if pt == anchor:
                    cv.circle(img, (pt[0], pt[1]), 7, (0,255,0), -1)
                else:
                    cv.circle(img, (pt[0], pt[1]), 9, (255,255,0), 2)
        cv.imshow("grid_display_img", img)