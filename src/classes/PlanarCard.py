import cv2 as cv
import numpy as np
import json
from util.capture import capture
from classes.AnswerDetector import AnswerDetector

class PlanarCard:
    def __init__(self, **kwargs):
        self.test_scene = kwargs['test_scene']
        self.dist_dir = kwargs['dist_dir']
        self.answer_detector = AnswerDetector(

        )

        timg = cv.imread("imgs/bubble-card.png")
        timg = cv.resize(timg, (465, 860))
        self.TRAIN_IMG = timg
        self.MIN_MATCH = 15

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
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0, (w,h))
        dst = cv.undistort(img, mtx, dist, None, newcameramtx)
        # dst = cv.resize(dst, (492,376))

        return dst

    def _match_points(self, t_img, q_img, min_match=10):
        t_img = cv.cvtColor(t_img, cv.COLOR_BGR2GRAY)
        sift = cv.SIFT_create()
        bf = cv.BFMatcher()
        timg_kp, timg_des = sift.detectAndCompute(t_img, mask=None)

        q_img = cv.cvtColor(q_img, cv.COLOR_BGR2GRAY)
        qimg_kp, qimg_des = sift.detectAndCompute(q_img, mask=None)

        if qimg_des is not None:
            matches = bf.knnMatch(timg_des, qimg_des, k=2)
            if len(matches[0]) == 1: return

            good = []
            for m,n in matches:
                if m.distance < n.distance * 0.7:
                    good.append(m)

            if len(good) >= min_match:
                train_pts = np.float32( [ timg_kp[m.queryIdx].pt for m in good ] ).reshape(-1, 1, 2)
                query_points = np.float32( [ qimg_kp[m.trainIdx].pt for m in good ] ).reshape(-1, 1, 2)
                return (train_pts, query_points)
            
    def _to_planar(self, from_img):
        points = self._match_points(self.TRAIN_IMG, from_img, min_match=self.MIN_MATCH)
        if points is None: return
        train_points, frame_points = points

        M, _ = cv.findHomography(train_points, frame_points, cv.RANSAC, 5.0)
        if M is not None:
            height, width = self.TRAIN_IMG.shape[0:2]
            pts = np.float32([ [0,0],[0,height-1],[width-1,height-1],[width-1,0] ]).reshape(-1,1,2)

            dst = cv.perspectiveTransform(pts, M)
            M2 = cv.getPerspectiveTransform(np.float32(dst), pts)
            warped = cv.warpPerspective(from_img, M2, (width, height))
            return warped
            
    def per_frame(self, src, copy, key_is):
        cv.imshow("src", src)
        dst = self._undistort(src)
        cv.imshow("dst", dst)

        planar_img = self._to_planar(dst)
        if planar_img is None: return  
        cv.imshow("planar", planar_img)
        answers = self.answer_detector.detect(planar_img)

        if self.test_scene is not None:
            cv.waitKey(0)