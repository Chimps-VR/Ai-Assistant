import os
import sys

def getResourcePath(filename):
    """ Get the correct path for files when using a frozen python file (aka python to exe file). """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, filename)