from classes.Initializer import Initializer
from util.path import get_path
from util.server import open_server
from threading import Thread

def main(**kwargs):
    if kwargs['comms'] == True:
        Thread(target=open_server).start()
    Initializer(**kwargs)

if __name__ == "__main__":
    main(
        test_scene=get_path("imgs/scenes/corner-bubs.jpg"),
        force_live=False,
        comms=False,
    )