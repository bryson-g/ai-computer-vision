import cv2 as cv
import numpy as np
from math import sqrt

class BubbleDetector():
    def __init__(self):
        pass

    def _get_circlish(self, contours):
        def cnt_to_pts(contours):
            points = []
            for cnt in contours:
                x, y, w, h = cv.boundingRect(cnt)
                cx = int(x+w/2)
                cy = int(y+h/2)
                points.append((cx, cy))
            return points    
        
        filtered = []
        for cnt in contours:
            approx = cv.approxPolyDP(cnt,0.01*cv.arcLength(cnt,True),True)
            _, _, w, h = cv.boundingRect(cnt)
            area = cv.contourArea(cnt)
            if ((len(approx) > 8) & (area > 150) ):
                pixels = max(w, h)
                if pixels < 30:
                    filtered.append(cnt)

        return cnt_to_pts(filtered)
    
    def _remove_too_close(self, points):
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
    
    def _remove_too_far(self, points):
        filtered = []

        for i1, pt1 in enumerate(points):
            smallest = 9999

            for i2, pt2 in enumerate(points):
                if i1 == i2: 
                    continue
                
                distance = sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)
                if distance < smallest:
                    smallest = distance

            if smallest < 45:
                filtered.append(pt1)

        return filtered
            

    def detect(self, img):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 15, 3)
        contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        circlish = self._get_circlish(contours)
        circlish = self._remove_too_close(circlish)
        circlish = self._remove_too_far(circlish)

        return circlish