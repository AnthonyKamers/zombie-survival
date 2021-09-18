import pygame as pg
from .Inimigo import Inimigo
from typing import List
from ..utils.functions import load_image

class Bala(pg.sprite.Sprite):
    def __init__(self, surface: pg.Surface, position, size, image, direction, dano: int = 25):
        super().__init__()
        self._surface = surface
        self._size = size
        self.image = load_image(image, size)

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position

        self._direction = direction
        self._dano = dano
    
    def getDano(self):
        return self._dano
    
    def checkCenario(cenario: pg.sprite.Sprite):
        pass

    def checkZumbi(zumbis: List):
        pass

    def destroy(self):
        pass

    def draw(self):
        self.rect.left += self._direction[0] * 2
        self.rect.top += self._direction[1] * 2
        self._surface.blit(self.image, (self.rect.left, self.rect.top))