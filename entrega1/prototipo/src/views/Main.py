import pygame as pg
import pytmx

from ..utils.functions import load_image, get_path
from ..personagens.Jogador import Jogador


class Tile(pg.sprite.Sprite):

    def __init__(self, surface, tile, posicao, tamanho):
        self.surface = surface
        self.x, self.y = posicao
        self.comprimento, self.altura = tamanho
        self.tile = tile

    def draw(self):
        self.surface.blit(self.tile, (self.x * self.comprimento, self.y * self.altura))

class Main():

    def __init__(self, surface, width, height):
        self._surface = surface
        self._player1 = Jogador(self._surface, width/2, height/2, 32, 32, imagem="player1.png")
        self._player2 = Jogador(self._surface, width/2, height/2, 32, 32, imagem="player2.png")

        self._vidas = pg.sprite.Group()

        self._cenario = pg.sprite.Group()
        self._layers = pytmx.load_pygame(get_path("map_finito.tmx"))

        for layer in self._layers.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self._layers.get_tile_image_by_gid(gid)
                    if tile:
                        tile = Tile(self._surface, pg.transform.scale(tile, (32, 32)), (x, y), (32, 32))
                        # self._cenario.add(tile)

        # montar base do cenário (com biblioteca pytmx)
        # for layer in layers.visible_layers:
        #     if isinstance(layer, pytmx.TiledTileLayer):
        #         self._cenario.append(layer)

        self._hud1 = load_image('hud1.png', (300, 150))
        self._hud2 = load_image('hud2.png', (300, 150))

    def play(self):
        pass

    def draw(self):
        self._cenario.draw(self._surface)

        # for layer in self._layers.visible_layers:
        #     if isinstance(layer, pytmx.TiledTileLayer):
        #         for x, y, gid in layer:
        #             tile = self._layers.get_tile_image_by_gid(gid)
        #             if tile:
        #                 self._surface.blit(pg.transform.scale(tile, (32, 32)), (x * self._layers.tilewidth * 0.5,
        #                 y * self._layers.tileheight * 0.5))
        
        # montagem do cenário
        # for layer in self._cenario:
        #     for x, y, gid in layer:
        #         tile = layer.get_tile_image_by_gid(gid)
        #         if tile:
        #             self.surface.blit(pg.transform.scale(tile, (32, 32)), (x * 32, y * 32))

        self._surface.blit(self._hud1, (0, 0))
        self._surface.blit(self._hud2, (724, 0))

        self._player1.draw()
        self._player2.draw()

        # for b in (self._player1.bullets() + self._player2.bullets()):
        #     b.draw()

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

        self._player1.move(direction[0], direction[1], self._cenario, self._vidas)

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

        self._player2.move(direction2[0], direction2[1], self._cenario, self._vidas)

        # tiro jogador 2
        if keyboard[pg.K_RCTRL] or keyboard[pg.K_LCTRL]:
            self._player2.shoot()

        # retorna parâmetro para Jogo
        return emit
