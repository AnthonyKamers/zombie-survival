from abc import ABC, abstractmethod
from utils.functions import utils

class Tela(ABC):
    def __init__(self, posicao: int, tamanho: int, imagem: str):
        self._posicao = posicao
        self._tamanho = tamanho
        self._imagem = utils.load_image(imagem)
    
    @abstractmethod
    def draw(self):
        pass
        