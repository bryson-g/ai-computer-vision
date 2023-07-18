from classes.Calibrator import Calibrator

def main(**kwargs):
    calibrator = Calibrator(**kwargs)
    if kwargs['capture_inputs']:
        calibrator.capture_inputs()
    calibrator.calibrate()

if __name__ == "__main__":
    main(
        capture_inputs=False,
        cycle_captures=False,
        grid=(6,9),
        input_dir="imgs/calib_inputs/",
        save_dir = "data/distortion.json"
    )