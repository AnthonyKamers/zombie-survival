import pygame as pg
import os

def get_path(path_file):
    path = os.path.split(os.getcwd())[0]
    return os.path.join(path, 'prototipo', 'images\\', path_file)

def load_image(path_image, size, convert=False):
    # path = os.path.join(os.path.dirname(__file__), 'images\\' + path)

    # path = os.path.split(os.getcwd())[0]
    # path = os.path.join(path, 'prototipo', 'images\\' + path_image)
    # print(path)

    image = pg.image.load(get_path(path_image))
    if convert:
        image = image.convert()
    else: 
        image = image.convert_alpha()

    return pg.transform.scale(image, size)
