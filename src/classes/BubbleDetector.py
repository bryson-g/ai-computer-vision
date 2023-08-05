import cv2 as cv
import numpy as np
from math import sqrt

class BubbleDetector():
    def __init__(self):
        params = cv.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = 250

        params.filterByConvexity = True
        params.minConvexity = .8
        params.maxConvexity = 1

        # params.filterByCircularity = True
        # params.minCircularity = .1
        # params.maxCircularity = 1
        
        self.blob_detector = cv.SimpleBlobDetector_create(params)

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
    
    def _get_blobs(self, img):
        copy = img.copy()
        copy = cv.cvtColor(copy, cv.COLOR_BGR2GRAY)
        
        keypoints = self.blob_detector.detect(copy)
        
        if True:
            for kp in keypoints:
                cv.circle(copy, (int(kp.pt[0]), int(kp.pt[1])), int(kp.size/2), 255, -1)

            draw_blobs = cv.drawKeypoints(copy, keypoints, None, (0, 255, 0), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            cv.imshow("bubbledetector_get_blobs_draw_blobs", draw_blobs)
        
        points = [kp.pt for kp in keypoints]
        return points
    
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

        blobs = self._get_blobs(img)

        circlish = self._get_circlish(contours)
        circlish = circlish + blobs

        circlish = self._remove_too_close(circlish)
        circlish = self._remove_too_far(circlish)

        return circlish, blobs