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

def flip_sprite(imagem, direction):
    if 0 not in direction: return imagem

    rotation = {
        (1,  0):  0,    # direita
        (-1, 0):  180,  # esquerda
        (0,  1): -90,   # cima
        (0, -1):  90    # baixo
    }

    return pg.transform.rotate(imagem, rotation[direction])