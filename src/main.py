from classes.Initializer import Initializer
from util.path import get_path

def main(**kwargs):
    Initializer(**kwargs)

if __name__ == "__main__":
    main(
        test_scene=get_path("imgs/scenes/0.9556373001096373.jpg"),
        force_live=False
    )