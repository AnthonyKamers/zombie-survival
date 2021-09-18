import pygame as pg
from .utils.constants import *


class Jogo:

    def __init__(self):
        self._surface = pg.display.set_mode((1024, 576))
        self._width, self._height = self._surface.get_size()
        self._paused = False
        self._game = None
        self._tick = pg.time.get_ticks()

        self._view = views["START"](self._surface) # setta view inicial para tela inicial

    def inicializarParametros(self):
        pg.init()
        pg.display.init()
        pg.display.set_caption("Zombie Survival")

    @property
    def getView(self):
        return self._view

    def drawView(self):
        self._view.draw()

    def unsetView(self):
        self._view = None

    def pausar(self):
        self._paused = True
        self._view = views["PAUSE"](self._surface)

    def iniciarPartida(self):
        self._game = views["MAIN"](self._surface, self._width, self._height)
        self._view = None

    def loop(self):
        # loop principal do jogo
        while True:
            # sair da aplicação
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
            
            pg.display.update()

            # troca de telas/views
            # quando jogo não estiver em execução
            if self._view is not None:
                target = self._view.draw()

                if target == 'RESUME':
                    self._view = None

                elif target in ("RESTART", "PLAY"):
                    self.iniciarPartida()

                elif target == 'EXIT':
                    self.quit()

            else:
                # view is none
                target = self._game.draw()

                if target == "PAUSE":
                    self.pausar()

                elif target == "isOver":
                    self._game = None
                    self._view = views["START"](self._surface)

    def quit(self):
        exit()