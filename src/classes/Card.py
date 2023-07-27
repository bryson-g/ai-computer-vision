import cv2 as cv
import numpy as np

from classes.Projector import Projector
from classes.BubbleDetector import BubbleDetector
from classes.Grid import Grid

class Card():
    def __init__(self, **kwargs):
        self.projector = Projector()
        self.bubble_detector = BubbleDetector()

    def per_frame(self, src, copy, key_is):
        projection = self.projector.planarize(copy)
        if projection is None: return
        points = self.bubble_detector.detect(projection)
        grid = Grid(points)
        grid.side_most(2, output_img=projection.copy())
        
        cv.imshow("card_per_frame_projection", projection)
        cv.imshow("card_per_frame_src", src)

        zeros = np.zeros_like(projection)
        for pt in points:
            cv.circle(zeros, (pt[0], pt[1]), 7, (0,255,0), 2)
        
        cv.imshow("card_per_frame_zeros", zeros)
        # cv.imshow("card_per_frame_projection", projection)