from classes.ParlayScanner import ParlayScanner

def main(**kwargs):
    scanner = ParlayScanner(**kwargs)

if __name__ == "__main__":
    main(
        test_scene=None,
        dist_dir="data/distortion.json"
    )