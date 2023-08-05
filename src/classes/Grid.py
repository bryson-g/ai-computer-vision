import cv2 as cv
import numpy as np
from math import sqrt

class Grid():
    def __init__(self, points, output_img=None):
        self.srt_pts = sorted(points, key=lambda  pt: pt[1])
        self.grid = []
        self._create(output_img)
    
    def _create(self, output_img):
        for pt in self.srt_pts:
            found_col = self._find_pt_column(pt)
            if not found_col:
                self.grid.append([pt])

        sides = self.side_most(2, output_img=output_img)
        if sides is not None:
            self.left, self.right = sides
            self.left = sorted(self.left, key=lambda pt: pt[1])
            self.right = sorted(self.right, key=lambda pt: pt[1])
        else:
            self.left, self.right = [],[]

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

        # both = left_cols + right_cols
        # for i1, pt1 in 

        # DISPLAY #
        if output_img is not None:
            img = output_img.copy()
            for grid in left_cols + right_cols:
                for pt in grid:
                    cv.circle(img, (int(pt[0]), int(pt[1])), 7, (0,255,0), 2)
            cv.imshow("grid_side_most_img", img)
        
        left = [pt for col in left_cols for pt in col]
        right = [pt for col in right_cols for pt in col]

        return (left, right)
    
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