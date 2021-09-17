import pygame as pg

class Teste(pg.sprite.Sprite):
    def __init__(self, surface, posicao, tamanho):
        self.rect = pg.Rect(posicao, tamanho)
        self.surface = surface
        self.x, self.y = posicao
        self.comprimento, self.altura = tamanho