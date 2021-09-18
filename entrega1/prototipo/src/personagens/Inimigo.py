import pygame as pg
import math

from typing import List
from .Personagem import Personagem
from .Teste import Teste

class Inimigo(Personagem, pg.sprite.Sprite):
    def __init__(self, surface: pg.Surface, x: int, y: int, comprimento: int, altura: int, vida: int = 100, velocidade: int = 1, imagem: str = "zumbi.png", dano: int = 1):
        super().__init__(surface, x, y, comprimento, altura, vida, velocidade, imagem)
        self._dano = dano
        self._jogador = None
        self._ultimoAtaque = 0
    
    def setJogadorInimigo(self, jogador):
        self._jogador = jogador

    def getDano(self):
        tickAtual = pg.time.get_ticks()
        if tickAtual - self._ultimoAtaque > 300:
            self._ultimoAtaque = tickAtual
            return self._dano
        else:
            return 0

    def getJogador(self):
        return self._jogador
    
    def getVida(self):
        return self._vida
    
    def reduzirVida(self, quantidadeVida: int):
        self._vida -= quantidadeVida

    def atingiuCenario(self, rect, walls):
        return pg.sprite.spritecollideany(self, walls)

    def move(self, walls):
        if self._jogador is None: return

        self.floating_point_x, self.floating_point_y = [
            self.rect.left, self.rect.top]
        self.dest_x, self.dest_y = (self._jogador.rect.left, self._jogador.rect.top)

        x_diff = self.dest_x - self.rect.left
        y_diff = self.dest_y - self.rect.top
        angle = math.atan2(y_diff, x_diff)

        self.change_x = math.cos(angle) * int(self._velocidade)
        self.change_y = math.sin(angle) * int(self._velocidade)

        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x

        self.rect.left = int(self.floating_point_x)
        self.rect.top = int(self.floating_point_y)

        positionBefore = (self.rect.left, self.rect.top)

        rect = Teste(self._surface, (int(self.floating_point_x), int(self.floating_point_y)), (self._comprimento, self._altura))
        collision = self.atingiuCenario(rect, walls)

        # colisao com parede
        if collision:
            self.rect.left = positionBefore[0]
            self.rect.top = positionBefore[1]
        else:
            self.rect.left = int(self.floating_point_x)
            self.rect.top = int(self.floating_point_y)