import pygame as pg
import pytmx
import random

from ..utils.functions import load_image, get_path
from ..personagens.Jogador import Jogador
from ..personagens.Inimigo import Inimigo

class Tile(pg.sprite.Sprite):

    def __init__(self, surface, tile, posicao, tamanho, name):
        super().__init__()
        self._surface = surface
        self._x, self._y = posicao
        self._comprimento, self._altura = tamanho
        self._tile = tile
        self._image = self._tile
        self._name = name
        self.rect = pg.Rect((self._x * self._comprimento, self._y * self._altura), tamanho)

    def getX(self):
        return self._x * self._comprimento
    
    def getY(self):
        return self._y * self._altura
    
    def getName(self):
        return self._name

    def draw(self):
        self._surface.blit(self._tile, (self._x * self._comprimento, self._y * self._altura))

class Main():

    def __init__(self, surface, width, height):
        self._surface = surface
        self._player1 = Jogador(self._surface, width/2, (height/2) - 100, 32, 32, imagem="player1.png")
        self._player2 = Jogador(self._surface, width/2, (height/2) - 100, 32, 32, imagem="player2.png")

        self._vidas = pg.sprite.Group()
        self._inimigos = pg.sprite.Group()
        self._cenario = []
        self._walls = pg.sprite.Group()
        self._layers = pytmx.load_pygame(get_path("map_finito.tmx"))

        self._tick = pg.time.get_ticks() # tick principal do jogo (tempo do jogo em andamento)
        self._iniciarRound = True

        self._round = 0
        self._qtdInimigosRound = 0

        # montar cenário
        for layer in self._layers.visible_layers:
            name = layer.name

            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self._layers.get_tile_image_by_gid(gid)
                    if tile:
                        tile = Tile(self._surface, pg.transform.scale(tile, (32, 32)), (x, y), (32, 32), name)
                        self._cenario.append(tile)
                        
                        if name == "wall":
                            self._walls.add(tile)

        # huds do jogo
        self._hud1 = load_image('hud1.png', (300, 150))
        self._hud2 = load_image('hud2.png', (300, 150))

        self.iniciarRound()

    def iniciarRound(self):
        pg.font.init()
        tick = pg.time.get_ticks()

        # Timer
        font = pg.font.SysFont('Arial', 64)

        if tick - self._tick >= 1000:
            self._tick = tick

            # self._qtdInimigosRound = random.randint(3, 15)
            self._qtdInimigosRound = 1
            cenario = list(filter(lambda x: x.getName() == 'floor', self._cenario))

            for i in range(0, self._qtdInimigosRound):
                escolhido = random.choice(cenario)
                inimigo_now = Inimigo(self._surface, escolhido.getX() + 50, escolhido.getY(), 32, 32, dano = self._round*2)
                inimigo_now.setJogadorInimigo(self._player1 if i % 2 == 0 else self._player2)
                
                self._inimigos.add(inimigo_now)

            return False
        else:
            timer = font.render(str(((tick - self._tick) // 1000) + 1), True, (255, 255, 0))
            self._surface.blit(timer, (self._surface.get_width() / 2, self._surface.get_height() / 2 - 200))
            return True


    def avaliarEncerramentoRound(self):
        if len(self._inimigos) == 0:
            self._iniciarRound = True
    
    def avaliarEncerramentoPartida(self):
        if self._player1._vida <= 0 or self._player2._vida <= 0:
            return True
    
    def collide(self):
        pass

    def draw(self):
        # blittar cenário na tela
        for i in self._cenario:
            i.draw()

        # blittar huds
        self._surface.blit(self._hud1, (0, 0))
        self._surface.blit(self._hud2, (724, 0))

        # blittar jogadores
        self._player1.draw()
        self._player2.draw()

        # blittar inimigos
        for inimigo in self._inimigos:
            inimigo.move(self._walls)
            inimigo.draw()

        # se hold estiver settada, deve executar método hold (3 segundos para jogadores se prepararem)
        if self._iniciarRound:
            self._iniciarRound = self.iniciarRound()

        # avalia se todos os zumbis foram mortos
        self.avaliarEncerramentoRound()

        # avaliar colisões do cenário / jogador / inimigo / bala
        self.collide()

        # avalia se um dos jogadores está morto
        isOver = self.avaliarEncerramentoPartida()
        isOver = "isOver" if isOver else self.event_listener()

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

        self._player1.move(direction[0], direction[1], self._walls, self._vidas)

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

        self._player2.move(direction2[0], direction2[1], self._walls, self._vidas)

        # tiro jogador 2
        if keyboard[pg.K_RCTRL] or keyboard[pg.K_LCTRL]:
            self._player2.shoot()

        # retorna parâmetro para Jogo
        return emit
