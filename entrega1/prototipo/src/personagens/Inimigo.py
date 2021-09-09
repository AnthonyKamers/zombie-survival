import pygame as pg
from typing import List
from Personagem import Personagem
from Jogador import Jogador

class Inimigo(Personagem, pg.sprite.Sprite):
    def __init__(self, x: int, y: int, comprimento: int, altura: int, vida: int, velocidade: int, direcao: List[int, int], imagem: str, dano: int):
        super().__init__(x, y, comprimento, altura, vida, velocidade, direcao, imagem)
        self._dano = dano
    
    @property
    def getDano(self):
        return self._dano
    
    def reduzirVida(self, quantidadeVida: int):
        self._vida -= quantidadeVida

    def move(self):
        pass
        