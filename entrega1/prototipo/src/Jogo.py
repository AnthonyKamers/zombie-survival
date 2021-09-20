import pygame as pg
from .utils.constants import *


class Jogo:

    def __init__(self):
        self._surface = pg.display.set_mode((1024, 576))
        self._comprimento, self._altura = self._surface.get_size()
        self._main = None
        self._view = None

    def inicializarParametros(self):
        self._view = views["START"](self._surface) # setta view inicial para tela inicial

        pg.init()
        pg.display.init()
        pg.display.set_caption("Zombie Survival")

    def drawView(self):
        return self._view.draw()

    def unsetView(self):
        self._view = None

    def pausar(self):
        self._view = views["PAUSE"](self._surface)

    def iniciarPartida(self):
        self.unsetView()
        self._main = views["MAIN"](self._surface, self._comprimento, self._altura)

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
                target = self.drawView()

                if target == 'RESUME':
                    self.unsetView()

                elif target in ("RESTART", "PLAY"):
                    self.iniciarPartida()

                elif target == 'EXIT':
                    self.quit()

            else:
                # view is none
                target = self._main.draw()

                if target == "PAUSE":
                    self.pausar()

                elif target == "isOver":
                    self._main = None
                    self._view = views["START"](self._surface)

    def quit(self):
        exit()