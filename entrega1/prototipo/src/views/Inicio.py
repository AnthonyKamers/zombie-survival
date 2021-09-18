import pygame as pg
from ..utils.functions import load_image
from .Tela import Tela

class Inicio(Tela):
    
    def __init__(self, surface: pg.Surface):
        super().__init__(surface, (1024, 576), "inicio.png")
        self._play = pg.Rect(512, 269, 366, 112)
        self._exit = pg.Rect(512, 440, 366, 112)
    
    def event_listener(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_click = pg.mouse.get_pressed()
    
        emit = ''
        if mouse_click[0]:
            if self._play.collidepoint(mouse_pos):
                emit = 'PLAY'
            elif self._exit.collidepoint(mouse_pos):
                emit = 'EXIT'
            
        return emit   
         
    def draw(self):
        self._surface.blit(self._image, (0, 0))
        return self.event_listener()