import pygame as pg

class Tile(pg.sprite.Sprite):

    def __init__(self, surface, tile, posicao, tamanho, name):
        super().__init__()
        self._surface = surface
        self._x, self._y = posicao
        self._comprimento, self._altura = tamanho
        self._tile = tile
        self._image = self._tile
        self._name = name
        self.rect = pg.Rect((self._x * self._comprimento, self._y * self._altura), tamanho)

    def getX(self):
        return self._x * self._comprimento
    
    def getY(self):
        return self._y * self._altura
    
    def getName(self):
        return self._name

    def draw(self):
        self._surface.blit(self._tile, (self._x * self._comprimento, self._y * self._altura))