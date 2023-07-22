import cv2 as cv
from util.capture import capture
from random import random

def take_picture():
    def per_frame(src, copy, key_is):
        cv.imshow("f to snap", src)
        if key_is('f'):
            cv.imwrite(f"imgs/scenes/{str(random())}.jpg", src)

    capture(per_frame)