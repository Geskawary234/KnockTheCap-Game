import os
import sys
import pyglet as pg

def resource_path(relative_path):
    """ Get absolute path to resource (compatible with PyInstaller) """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def LoadAsset(filename):
    return pg.image.load(resource_path(filename))

def LoadAudio(filename):
    return pg.media.load(resource_path(filename), streaming=False)
