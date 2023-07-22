from classes.PlanarCard import PlanarCard

def main(**kwargs):
    scanner = PlanarCard(**kwargs)

if __name__ == "__main__":
    main(
        test_scene=None,
        dist_dir="data/distortion.json"
    )