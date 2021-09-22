import pygame as pg

from .Personagem import Personagem
from .Bala import Bala
from .Teste import Teste # classe auxiliar para fazer teste de colisão com parede
from ..utils import functions

class Jogador(Personagem):

    def __init__(self, surface: pg.Surface, x: int, y: int, comprimento: int, altura: int, vida: int = 100, velocidade: int = 1, imagem: str = "player1.png"):
        super().__init__(surface, x, y, comprimento, altura, vida, velocidade, imagem)
        self._balas = pg.sprite.Group()

        self._direcao = [1, 0]
        self._lastDirecao = [1, 0]
        self._intervaloDeTiro = 200
        self._ultimoTiro = pg.time.get_ticks()
    
    def move(self, x: int, y: int, cenario: pg.sprite.Sprite):
        direction = [x, y]

        # teste de colisão com o cenário
        rect = Teste((self.rect.left + direction[0], self.rect.top + direction[1]), (self._comprimento, self._altura))
        atingiuCenario = self.atingiuCenario(rect, cenario)

        # se não colidiu com o cenário, movimenta-se
        if not atingiuCenario:
            self.rect.left += direction[0]
            self.rect.top += direction[1]

            # atualizar dados de movimento do jogador (para dar hold on no estado do tiro)
            self._direcao = direction

            if direction[0] or direction[1]:
                self._lastDirecao = self._direcao

    def shoot(self):
        tickAtual = pg.time.get_ticks()
        if tickAtual - self._ultimoTiro > self._intervaloDeTiro:
            self._ultimoTiro = tickAtual
            self._balas.add(Bala(self._surface, (self.rect.left, self.rect.top), (5, 5), 'bala.png', self._lastDirecao))

    def getVida(self):
        return self._vida
    
    def getBalas(self):
        return self._balas

    def reduzirVida(self, quantidadeVida: int):
        self._vida -= quantidadeVida

    def atingiuCenario(self, rect, walls):
        return pg.sprite.spritecollideany(rect, walls)

    def draw(self):
        self._surface.blit(functions.flip_sprite(self._image, tuple(self._lastDirecao)), (self.rect.left, self.rect.top))

        # blittar balas do jogador
        for bala in self._balas:
            bala.draw()