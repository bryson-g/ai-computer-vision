import cv2 as cv
import numpy as np
from util.capture import capture
from classes.Card import Card

class Initializer():
    def __init__(self, **kwargs):
        self.test_scence = kwargs['test_scene']
        self.card = Card(**kwargs)
        self._create_window()
        self._handle_result()

    def _create_window(self):
        img = np.zeros((115,500,3))
        font = cv.FONT_HERSHEY_PLAIN
        org = (0,50)
        thickness = 2

        img = cv.putText(img, "PRESS A FOR LIVE", org, font, 3, (0,255,0), thickness, cv.LINE_AA)
        img = cv.putText(img, "PRESS D FOR TEST", (org[0], org[1]+50), font, 3, (0,0,255), thickness, cv.LINE_AA)
        cv.imshow("initializer_create_window_img", img)

    def _handle_result(self):
        key = cv.waitKey(0) & 0xFF
        cv.destroyAllWindows()

        if key == ord('a'):
            capture(self.card.per_frame)
        elif key == ord('d'):
            capture(self.card.per_frame, test_scene=self.test_scence)