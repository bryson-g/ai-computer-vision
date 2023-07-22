from classes.PlanarCard import PlanarCard

def main(**kwargs):
    scanner = PlanarCard(**kwargs)
    scanner.scan()

if __name__ == "__main__":
    main(
        test_scene="imgs/scenes/parlay-curve.jpg",
        dist_dir="data/distortion.json"
    )