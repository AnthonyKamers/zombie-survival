import pygame as pg
from Inimigo import Inimigo
from typing import List
from utils.functions import utils

class Bala:
    def __init__(self, dano: int):
        self._dano = dano
        self._trajetoria = ()
    
    @property
    def getDano(self):
        return self._dano
    
    def checkCenario(cenario: pg.Sprite):
        pass

    def checkZumbi(zumbis: List[Inimigo]):
        pass

    def destroy(self):
        pass

class Bullet(pg.sprite.Sprite):
    def __init__(self, surface: pg.Surface, position, size, image, direction):
        self._surface = surface
        self._size = size
        self._image = utils.load_image(image, size)
        self._rect = self._image.get_rect()

        self._rect.left, self._rect.top = position
        self._direction = direction
    
    def update(self):
        pass

    def draw(self):
        self._rect.left += self._direction[0]
        self._rect.top += self._direction[1]
        self._surface.blit(self._image, (self._rect.left, self._rect.top))