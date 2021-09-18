import pygame as pg
from ..utils.functions import load_image
from .Tela import Tela

class Pause(Tela):

    def __init__(self, surface: pg.Surface):
        super().__init__(surface, (1024, 576), "pause.png")
        self._resume = pg.Rect(512, 210, 366, 112)
        self._restart = pg.Rect(512, 358, 366, 112)
        self._exit = pg.Rect(512, 495, 366, 112)
    
    def event_listener(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_click = pg.mouse.get_pressed()

        if mouse_click[0]:
            emit = ''
            if self._resume.collidepoint(mouse_pos):
                emit = 'RESUME'
            elif self._restart.collidepoint(mouse_pos):
                emit = 'RESTART'
            elif self._exit.collidepoint(mouse_pos):
                emit = 'EXIT'
            
            return emit
    
    def draw(self):
        self._surface.blit(self._image, (0, 0))
        return self.event_listener()