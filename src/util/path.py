import time
import os
import sys

def get_path(path):
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        return os.path.join(application_path, path)
    elif __file__:
        return path