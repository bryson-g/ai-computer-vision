import cv2 as cv
import numpy as np
from math import sqrt

from constants import answers

class Answers():
    def __init__(self, left, right, blobs):
        left_ans = self._calculate_side(left, blobs, answers.left)
        right_ans = self._calculate_side(right, blobs, answers.right)
        # self.final = left_ans + right_ans
        self.final = self._calculate_index(left + right, blobs)


    def _calculate_side(self, pts, blobs, answers):
        side_answers = []

        for i, pt in enumerate(pts):
            for blob in blobs:
                distance = sqrt((pt[0] - blob[0])**2 + (pt[1] - blob[1])**2)
                if distance < 7:
                    side_answers.append(answers[i])

        return side_answers
    
    def _calculate_index(self, pts, blobs):
        i_answers = []

        for i, pt in enumerate(pts):
            for blob in blobs:
                distance = sqrt((pt[0] - blob[0])**2 + (pt[1] - blob[1])**2)
                if distance < 7:
                    i_answers.append(i)

        return i_answers      