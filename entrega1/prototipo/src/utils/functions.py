import pygame as pg
import os


def load_image(path, size, convert=False):
    path = os.path.join(os.path.dirname(__file__), 'images\\' + path)

    image = pg.image.load(path)
    if convert:
        image = image.convert()
    else: 
        image = image.convert_alpha()

    return pg.transform.scale(image, size)
