import pygame as pg
from typing import List
from .Personagem import Personagem

class Inimigo(Personagem, pg.sprite.Sprite):
    def __init__(self, surface: pg.Surface, x: int, y: int, comprimento: int, altura: int, vida: int, velocidade: int, imagem: str, dano: int):
        super().__init__(surface, x, y, comprimento, altura, vida, velocidade, imagem)
        self._dano = dano
        self._jogador = None
    
    @property
    def getDano(self):
        return self._dano
    
    def reduzirVida(self, quantidadeVida: int):
        self._vida -= quantidadeVida

    def move(self):
        pass
        