import pygame as pg
from utils.functions import load_image
from personagens import Personagem


class Main():

    def __init__(self, surface, width, height):
        self._surface = surface
        self._player1 = Personagem(self._surface, (width/2, height/2), (32, 32), "player1.png")
        self._player2 = Personagem(self._surface, (width/2, height/2), (32, 32), "player2.png")
        self._image = load_image('map.png', (1024, 576))

        self._hud1 = load_image('hud1.png', (300, 150))
        self._hud2 = load_image('hud2.png', (300, 150))

    def play(self):
        pass

    def draw(self):
        self._surface.blit(self._image, (0, 0)) # blittar fundo (cenário)
        self._surface.blit(self._hud1, (0, 0))
        self._surface.blit(self._hud2, (724, 0))

        self._player1.draw()
        self._player2.draw()

        for b in (self._player1.bullets() + self._player2.bullets()):
            b.draw()

        self.update()

        # eventos gerais do jogo (input usuário)
        return self.event_listener()

    def update(self):
        pass

    def event_listener(self):
        keyboard = pg.key.get_pressed()

        emit = ""

        # pause do jogo
        if keyboard[pg.K_p]:
            emit = "PAUSE"
            return emit

        # jogador 1
        direction = [0, 0]
        if keyboard[pg.K_a]:
            direction[0] = -1
        elif keyboard[pg.K_d]:
            direction[0] = 1

        if keyboard[pg.K_w]:
            direction[1] = -1
        elif keyboard[pg.K_s]:
            direction[1] = 1

        self._player1.move(direction)

        # tiro jogador 1
        if keyboard[pg.K_SPACE]:
            self._player1.shoot()

        # jogador 2
        direction2 = [0, 0]
        if keyboard[pg.K_LEFT]:
            direction2[0] = -1
        elif keyboard[pg.K_RIGHT]:
            direction2[0] = 1

        if keyboard[pg.K_UP]:
            direction2[1] = -1
        elif keyboard[pg.K_DOWN]:
            direction2[1] = 1

        self._player2.move(direction2)

        # tiro jogador 2
        if keyboard[pg.K_RCTRL] or keyboard[pg.K_LCTRL]:
            self._player2.shoot()

        # retorna parâmetro para Game
        return emit
