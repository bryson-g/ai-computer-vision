import cv2 as cv

def capture(per_frame, cap_size=None):
    cap = cv.VideoCapture(0)

    # 3840x2160 native
    if cap_size is not None:
        cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_size[0])
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_size[1])

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