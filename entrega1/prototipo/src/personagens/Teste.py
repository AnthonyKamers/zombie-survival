import pygame as pg

class Teste(pg.sprite.Sprite):
    def __init__(self, posicao, tamanho):
        self.rect = pg.Rect(posicao, tamanho)