from classes.ParlayCard import ParlayCard

def main(**kwargs):
    scanner = ParlayCard(**kwargs)
    scanner.scan()

if __name__ == "__main__":
    main(
        # test_scene=None,
        test_scene="imgs/scenes/parlay-curve.jpg",
        dist_dir="data/distortion.json"
    )