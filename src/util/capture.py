import cv2 as cv

def capture(per_frame):
    cap = cv.VideoCapture(0)

    while True:
        _, frame = cap.read()
        key = cv.waitKey(1)

        def key_is(compare):
            if key & 0xFF == ord(compare):
                return True

        per_frame(frame, frame.copy(), key_is)

        if key_is('q'):
            break

    cap.release()
    cv.destroyAllWindows()