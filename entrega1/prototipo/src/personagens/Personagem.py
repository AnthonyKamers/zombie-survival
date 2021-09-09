from abc import ABC, abstractmethod
from typing import List
from utils.functions import utils

class Personagem(ABC):
    def __init__(self, x: int, y: int, comprimento: int, altura: int, vida: int, velocidade: int, direcao: List[int, int], imagem: str):
        self._x = x
        self._y = y
        self._comprimento = comprimento
        self._altura = altura
        self._vida = vida
        self._velocidade = velocidade
        self._direcao = direcao
        self._imagem = utils.load_image(imagem, (comprimento, altura))
        self.rect = self._imagem.get_rect()
    
    @abstractmethod
    def move(self):
        pass
