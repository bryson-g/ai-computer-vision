import cv2 as cv
import numpy as np
from classes.Grid import Grid
import constants.answers as answer_list
from math import sqrt

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
        
        if display:
            for kp in keypoints:
                cv.circle(copy, (int(kp.pt[0]), int(kp.pt[1])), int(kp.size/2), 255, -1)

            copy = cv.drawKeypoints(copy, keypoints, None, (0, 255, 0), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            cv.imshow("drawn", copy)
        
        return keypoints
    
    def _merge_cols(self, cols):
        ret_pts = []

        for col in cols:
            for pt in col:
                ret_pts.append(pt)

        ret_pts = sorted(ret_pts, key=lambda pt: pt[1])
        return ret_pts

    def _side_answers(self, blob_kp, bubbles, comp_answers, debug_img=None):
        answers = []    

        for i, bubb_pt in enumerate(bubbles):
            for bkp in blob_kp:
                copy = None
                if debug_img is not None:
                    copy = debug_img.copy()

                distance = sqrt((bubb_pt[0] - bkp.pt[0])**2 + (bubb_pt[1] - bkp.pt[1])**2)

                if debug_img is not None:
                    print(distance, bkp.size/2)

                if distance < bkp.size/2:
                    answers.append(comp_answers[i])

                if copy is not None:
                    cv.circle(copy, (int(bkp.pt[0]), int(bkp.pt[1])), 7, 255, 2)
                    cv.circle(copy, (bubb_pt[0], bubb_pt[1]), 5, (0,255,0), 3)
                    cv.imshow("answerdetector_side_answers_debug_img", copy)
                    cv.waitKey(0)

        return answers

    def _answers(self, blob_kp, left_cols, right_cols, img):
        left_bubbles = self._merge_cols(left_cols)
        right_bubbles = self._merge_cols(right_cols)
        
        right_answers = self._side_answers(blob_kp, right_bubbles, answer_list.right, debug_img=None)
        left_answers = self._side_answers(blob_kp, left_bubbles, answer_list.left, debug_img=None)
                
        return right_answers + left_answers

    
    def _expected_amount(self, cols):
        if cols is None:
            return False

        count = 0
        for side in cols:
            for col in side:
                count += len(col)

        return count == 46
    
    def _blob_perfectify(self, img, blobs, debug_display=True):
        img = img.copy()

        for bkp in blobs:
            cv.circle(img, (int(bkp.pt[0]), int(bkp.pt[1])), 10, (0,255,255), 2)
        
        if debug_display:
            cv.imshow("answerdetecor_blob_perfectify_img", img)
            cv.waitKey(0)

        return img


    def detect(self, img):
        blob_kp = self._get_blobs(img, display=True)
        img = self._blob_perfectify(img, blob_kp, debug_display=False)

        points = self._get_circlish(img)
        grid = Grid(points)
        side_cols = grid.side_most(2, output_img=img)

        if self._expected_amount(side_cols):
            left_cols, right_cols = side_cols
            answers = self._answers(blob_kp, left_cols, right_cols, img)
            print(answers)