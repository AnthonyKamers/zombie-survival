import pygame as pg
import pytmx
import random

from ..utils.functions import load_image, get_path
from ..personagens.Jogador import Jogador
from ..personagens.Inimigo import Inimigo
from .Tile import Tile

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

        pg.font.init()
        self.iniciarRound()

    def iniciarRound(self):
        tick = pg.time.get_ticks()

        # Timer
        font = pg.font.SysFont('Arial', 64)

        if tick - self._tick >= 3000:
            self._tick = tick

            self._round += 1

            self._qtdInimigosRound = random.randint(3, 7)
            cenario = list(filter(lambda x: x.getName() == 'spawnpoints', self._cenario))

            for i in range(0, self._qtdInimigosRound):
                escolhido = random.choice(cenario)
                inimigo_now = Inimigo(self._surface, escolhido.getX(), escolhido.getY(), 32, 32, dano = (self._round+1)*2)
                inimigo_now.setJogadorInimigo(self._player1 if i % 2 == 0 else self._player2)
                
                self._inimigos.add(inimigo_now)

            return False
        else:
            timer = font.render(str(3 - ((tick - self._tick) // 1000)), True, (255, 255, 0))
            self._surface.blit(timer, (self._surface.get_width() / 2, self._surface.get_height() / 2 - 200))
            return True

    def avaliarEncerramentoRound(self):
        if len(self._inimigos) == 0:
            self._iniciarRound = True
    
    def avaliarEncerramentoPartida(self):
        if self._player1.getVida() <= 0 or self._player2.getVida() <= 0:
            return "isOver"
        return ""
    
    def collideInimigoBala(self, jogador):
        colisao = pg.sprite.groupcollide(self._inimigos, jogador.getBalas(), False, True)
        for inimigo, bala in colisao.items():
            inimigo.reduzirVida(bala[0].getDano())

            # se vida do inimigo for <= 0, matar
            if inimigo.getVida() <= 0:
                self._inimigos.remove(inimigo)

    def collideJogadorInimigo(self, jogador):
        inimigo = pg.sprite.spritecollideany(jogador, self._inimigos)
        if inimigo is not None:
            jogador.reduzirVida(inimigo.getDano())

    def collide(self):
        # colisão dos inimigos com o jogador
        self.collideJogadorInimigo(self._player1)
        self.collideJogadorInimigo(self._player2)

        # colisão balas dos jogadores com as paredes (e destruir as balas, caso atingirem)
        pg.sprite.groupcollide(self._walls, self._player1.getBalas(), False, True)
        pg.sprite.groupcollide(self._walls, self._player2.getBalas(), False, True)
        
        # colisão balas dos jogadores com inimigos
        self.collideInimigoBala(self._player1)
        self.collideInimigoBala(self._player2)

    def draw(self):
        # blittar cenário na tela
        for i in self._cenario:
            i.draw()
        
        # blittar round atual
        font = pg.font.SysFont('Arial', 64)
        round = font.render(str(self._round), True, (0, 0, 0))
        self._surface.blit(round, (self._surface.get_width() / 2, 0))

        # blittar jogadores
        self._player1.draw()
        self._player2.draw()

        # blittar vida jogadores
        vida1 = font.render("P1: " + str( + self._player1.getVida()), True, (0, 0, 0))
        vida2 = font.render("P2: " + str(self._player2.getVida()), True, (0, 0, 0))
        self._surface.blit(vida1, (5, 0))
        self._surface.blit(vida2, (self._surface.get_width() - 190, 0))

        # blittar inimigos
        for inimigo in self._inimigos:
            inimigo.move(self._walls)
            inimigo.draw()

        # se atributo estiver settado, deve executar método iniciarRound (3 segundos para jogadores se prepararem)
        if self._iniciarRound:
            self._iniciarRound = self.iniciarRound()

        # avalia se todos os zumbis foram mortos
        self.avaliarEncerramentoRound()

        # avaliar colisões do cenário / jogador / inimigo / bala
        self.collide()

        # avalia se um dos jogadores está morto
        isOver = self.avaliarEncerramentoPartida()

        return isOver or self.event_listener()

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
