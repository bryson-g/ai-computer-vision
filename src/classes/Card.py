import cv2 as cv
import numpy as np

from classes.Projector import Projector
from classes.BubbleDetector import BubbleDetector
from classes.Grid import Grid
from classes.Answers import Answers
from classes.Barcode import Barcode


class Card():
    def __init__(self, **kwargs):
        self.projector = Projector()
        self.bubble_detector = BubbleDetector()
        self.barcode = Barcode()

    def per_frame(self, src, copy, key_is):
        projection, undistorted = self.projector.planarize(copy)
        if projection is None: return
        points, blobs = self.bubble_detector.detect(projection)
        grid = Grid(points, output_img=projection.copy())

        if len(grid.left) + len(grid.right) == 46:
            answers = Answers(grid.left, grid.right, blobs)
            self.barcode.scan(projection)
            print(answers.final)

        cv.imshow("card_per_frame_projection", projection)
        cv.imshow("card_per_frame_undistorted", undistorted)
        zeros = np.zeros_like(projection)
        for pt in points:
            cv.circle(zeros, (int(pt[0]), int(pt[1])), 7, (0,255,0), 2)
        
        cv.imshow("card_per_frame_zeros", zeros)