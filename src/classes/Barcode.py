import cv2 as cv
from pylibdmtx.pylibdmtx import decode

class Barcode():

    @staticmethod
    def scan(planar):
        roi = planar[630:740, 170:290]
        cv.imshow("barcode_scan_roi", roi)
        
        codes = decode(roi)
        if codes:
            data = codes[0].data.decode('utf-8')
            return data