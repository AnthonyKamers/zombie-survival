import math
import pygame as pg

from typing import List
from Personagem import Personagem
from Inimigo import Inimigo
from Bala import Bala
from utils.functions import utils

class Jogador(Personagem, pg.sprite.Sprite):
    def __init__(self, x: int, y: int, comprimento: int, altura: int, vida: int, velocidade: int, direcao: List[int, int], imagem: str):
        super().__init__(x, y, comprimento, altura, vida, velocidade, direcao, imagem)
        self._balas = []

        self._direcao = [0, 0]
        self._lastDirecao = [0, 0]
    
    def move(self, x: int, y: int, cenario: pg.sprite.Sprite, vidas: pg.sprite.Group):
        direction = [x, y]

        # teste de colisão com o cenário
        rect = pg.Rect(self.rect.left + direction[0], self.rect.top + direction[1], self._comprimento, self._altura)
        atingiuCenario = self.atingiuCenario(rect, cenario)

        # se não colidiu com o cenário, movimenta-se
        if not atingiuCenario:
            self.rect.left += direction[0]
            self.rect.top += direction[1]

            # atualizar dados de movimento do jogador (para dar hold on)
            self._direcao = direction

            if direction[0] or direction[1]:
                self._lastDirecao = self._direcao

        # teste de colisão com alguma vida
        vidaAtingida = self.atingiuVida(vidas)
        if vidaAtingida is not None:
            vidas.remove(vidaAtingida)  # remove curativo do cenário
            self.aumentarVida(10)       # cada curativo tem recuperação de vida de 10% da vida do jogador

            

    def shoot(self):
        self.__floating_point_x, self.__floating_point_y = self.rect.left, self.rect.top
        self.__dest_x, self.__dest_y = destination

        x_diff = self.__dest_x - self.rect.left
        y_diff = self.__dest_y - self.rect.top
        angle = math.atan2(y_diff, x_diff)

        self.__change_x = math.cos(angle) * int(self.speed)
        self.__change_y = math.sin(angle) * int(self.speed)

    @property
    def getVida(self):
        return self._vida
    
    @property
    def getPosicao(self):
        return (self._x, self._y)
    
    @property
    def getBalas(self):
        return self._balas
    
    def aumentarVida(self, quantidadeVida: int):
        self._vida += quantidadeVida

    def reduzirVida(self, quantidadeVida: int):
        self._vida -= quantidadeVida
    
    # def checkZumbi(self, zumbis: List[Inimigo]):
    #     pass

    def atingiuCenario(self, rect: pg.Rect, cenario: pg.Sprite):
        return pg.sprite.spritecollideany(rect, cenario) is not None

    def atingiuVida(self, vidas: pg.Sprite):
        return pg.sprite.spritecollideany(self, vidas)


class Character(pg.sprite.Sprite):
    def __init__(self, surface: pg.Surface, position, size, image):
        self._surface = surface
        self._size = size
        self._image = utils.load_image(image, size)
        self.rect = self.image.get_rect()
        self._rect.left, self._rect.top = position

        self._lastDirection = [0, 0]
        self._direction = [0, 0]

        self._bullets = []

    def update(self):
        pass

    def draw(self):
        self._surface.blit(self._image, (self._rect.left, self._rect.top))
        self.update()

    def move(self, direction):
        self._direction = direction

        if direction[0] or direction[1]:
            self._lastDirection = self._direction

        self._rect.left += direction[0]
        self._rect.top += direction[1]

    def shoot(self):
        self._bullets.append(Bullet(self._surface, (self._rect.left, self._rect.top), (5, 5), 'bala.png', self._lastDirection))
    
    def bullets(self):
        return self._bullets
        