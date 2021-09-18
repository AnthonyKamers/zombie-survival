import pygame as pg

from abc import ABC, abstractmethod
from ..utils.functions import load_image

class Tela(ABC):
    def __init__(self, surface: pg.Surface ,size: int, image: str):
        self._surface = surface
        self._image = load_image(image, size)
    
    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def event_listener(self):
        pass