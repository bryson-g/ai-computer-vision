import cv2 as cv
import numpy as np
import requests

from classes.Projector import Projector
from classes.BubbleDetector import BubbleDetector
from classes.Grid import Grid
from classes.Answers import Answers
from classes.Barcode import Barcode


class Card():
    def __init__(self, **kwargs):
        self.projector = Projector()
        self.bubble_detector = BubbleDetector()
        self.comms = kwargs['comms']

    def _send_answers(self, id, indexes):
        url = f"http://localhost:8096/?Command=ParlayCardScan&ID={id}&Selections={'.'.join(indexes)}"

        try:
            print("Sending request to: ", url)
            requests.post(url)
        except Exception as e:
            print("HTTP request failed.")

    def per_frame(self, src, copy, key_is):
        projection, undistorted = self.projector.planarize(copy)
        cv.imshow("card_per_frame_undistorted", undistorted)
        cv.setWindowProperty("card_per_frame_undistorted", cv.WND_PROP_TOPMOST, 1)

        if projection is None: return
        points, blobs = self.bubble_detector.detect(projection)
        grid = Grid(points, output_img=projection.copy())

        if len(grid.left) + len(grid.right) == 46:
            answers = Answers(grid.left, grid.right, blobs)
            data = Barcode.scan(projection)
            print(data, answers.final)

            if self.comms == True:
                self._send_answers(data, answers.final)

        cv.imshow("card_per_frame_projection", projection)
        zeros = np.zeros_like(projection)
        for pt in points:
            cv.circle(zeros, (int(pt[0]), int(pt[1])), 7, (0,255,0), 2)
        cv.imshow("card_per_frame_zeros", zeros)