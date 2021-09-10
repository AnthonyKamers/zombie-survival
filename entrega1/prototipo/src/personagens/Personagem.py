import pygame as pg
from abc import ABC, abstractmethod
from typing import List
from ..utils.functions import load_image

class Personagem(ABC):
    def __init__(self, surface: pg.Surface, x: int, y: int, comprimento: int, altura: int, vida: int, velocidade: int, imagem: str):
        self._surface = surface
        self._x = x
        self._y = y
        self._comprimento = comprimento
        self._altura = altura
        self._vida = vida
        self._velocidade = velocidade
        self._imagem = load_image(imagem, (comprimento, altura))
        self.rect = self._imagem.get_rect()
    
    @abstractmethod
    def move(self):
        pass

    def draw(self):
        self._surface.blit(self._image, (self._rect.left, self._rect.top))
