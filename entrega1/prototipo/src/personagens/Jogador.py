import math
import pygame as pg

from typing import List
from .Personagem import Personagem
from .Inimigo import Inimigo
from .Bala import Bala
from .Teste import Teste
from ..utils import functions

class Jogador(Personagem, pg.sprite.Sprite):

    def __init__(self, surface: pg.Surface, x: int, y: int, comprimento: int, altura: int, vida: int = 100, velocidade: int = 1, imagem: str = "player1.png"):
        super().__init__(surface, x, y, comprimento, altura, vida, velocidade, imagem)
        self._balas = pg.sprite.Group()

        self._direcao = [1, 0]
        self._lastDirecao = [1, 0]
    
    def move(self, x: int, y: int, cenario: pg.sprite.Sprite, vidas: pg.sprite.Group):
        direction = [x, y]

        # teste de colisão com o cenário
        # rect = pg.Rect(self.rect.left + direction[0], self.rect.top + direction[1], self._comprimento, self._altura)
        rect = Teste(self._surface, (self.rect.left + direction[0], self.rect.top + direction[1]), (self._comprimento, self._altura))
        atingiuCenario = self.atingiuCenario(rect, cenario)

        # se não colidiu com o cenário, movimenta-se
        if not atingiuCenario:
            self.rect.left += direction[0]
            self.rect.top += direction[1]

            # atualizar dados de movimento do jogador (para dar hold on no estado do tiro)
            self._direcao = direction

            if direction[0] or direction[1]:
                self._lastDirecao = self._direcao

        # teste de colisão com alguma vida
        vidaAtingida = self.atingiuVida(vidas)
        if vidaAtingida is not None:
            vidas.remove(vidaAtingida)  # remove curativo do cenário
            self.aumentarVida(10)       # cada curativo tem recuperação de vida de 10% da vida do jogador

    def shoot(self):
        self._balas.add(Bala(self._surface, (self.rect.left, self.rect.top), (5, 5), 'bala.png', self._lastDirecao))

    def getVida(self):
        return self._vida
    
    def getPosicao(self):
        return (self._x, self._y)
    
    def getBalas(self):
        return self._balas
    
    def aumentarVida(self, quantidadeVida: int):
        self._vida += quantidadeVida

    def reduzirVida(self, quantidadeVida: int):
        self._vida -= quantidadeVida

    def checkZumbi(self, zumbis):
        # for zumbi in zumbis:
        pass

    def atingiuCenario(self, rect, walls):
        return  pg.sprite.spritecollideany(rect, walls)

    def atingiuVida(self, vidas: pg.sprite.Sprite):
        return pg.sprite.spritecollideany(self, vidas)

    def draw(self):
        self._surface.blit(functions.flip_sprite(self._imagem, tuple(self._lastDirecao)), (self.rect.left, self.rect.top))
        
        # blittar balas do jogador
        for b in self._balas:
            b.draw()


# class Character(pg.sprite.Sprite):
#     def __init__(self, surface: pg.Surface, position, size, image):
#         self._surface = surface
#         self._size = size
#         self._image = utils.load_image(image, size)
#         self.rect = self.image.get_rect()
#         self._rect.left, self._rect.top = position

#         self._lastDirection = [0, 0]
#         self._direction = [0, 0]

#         self._bullets = []

#     def update(self):
#         pass

#     def draw(self):
#         self._surface.blit(self._image, (self._rect.left, self._rect.top))
#         self.update()

#     def move(self, direction):
#         self._direction = direction

#         if direction[0] or direction[1]:
#             self._lastDirection = self._direction

#         self._rect.left += direction[0]
#         self._rect.top += direction[1]

#     def shoot(self):
#         self._bullets.append(Bala(self._surface, (self._rect.left, self._rect.top), (5, 5), 'bala.png', self._lastDirection))
    
#     def bullets(self):
#         return self._bullets
        