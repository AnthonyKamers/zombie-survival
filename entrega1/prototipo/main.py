from abc import ABC, abstractmethod

import pygame as pg
import os

def load_image(path, size, convert=False):
    path = os.path.join(os.path.dirname(__file__), 'images\\' + path)

    image = pg.image.load(path)
    if convert:
        image = image.convert()
    else: 
        image = image.convert_alpha()

    return pg.transform.scale(image, size)

class Bullet(pg.sprite.Sprite):
    def __init__(self, surface: pg.Surface, position, size, image, direction):
        self._surface = surface
        self._size = size
        self._image = load_image(image, size)
        self._rect = self._image.get_rect()

        self._rect.left, self._rect.top = position
        self._direction = direction
    
    def update(self):
        pass

    def draw(self):
        self._rect.left += self._direction[0]
        self._rect.top += self._direction[1]
        self._surface.blit(self._image, (self._rect.left, self._rect.top))

class Character(pg.sprite.Sprite):
    def __init__(self, surface: pg.Surface, position, size, image):
        self._surface = surface
        self._size = size
        self._image = load_image(image, size)
        self._rect = self._image.get_rect()
        self._rect.left, self._rect.top = position

        self._lastDirection = [0, 0]
        self._direction = [0, 0]

        self._bullets = []

    def update(self):
        pass

    def draw(self):
        self._surface.blit(self._image, (self._rect.left, self._rect.top))
        self.update()

    def move(self, direction):
        self._direction = direction

        if direction[0] or direction[1]:
            self._lastDirection = self._direction

        self._rect.left += direction[0]
        self._rect.top += direction[1]

    def shoot(self):
        self._bullets.append(Bullet(self._surface, (self._rect.left, self._rect.top), (5, 5), 'bala.png', self._lastDirection))
    
    def bullets(self):
        return self._bullets
class StartView():
    def __init__(self, surface: pg.Surface):
        self._surface = surface
        self._image = load_image("inicio.png", (1024, 576))
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

    def update(self):
        pass
        
class PauseView():
    def __init__(self, surface: pg.Surface):
        self._surface = surface
        self._image = load_image("pause.png", (1024, 576))
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

    def update(self):
        pass

class MainView():
    def __init__(self, surface, width, height):
        self._surface = surface
        self._player1 = Character(self._surface, (width/2, height/2), (32, 32), "player1.png")
        self._player2 = Character(self._surface, (width/2, height/2), (32, 32), "player2.png")
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

views = {
    "PAUSE": PauseView,
    "START": StartView,
    "MAIN": MainView
}

class Game: 
    def __init__(self):
        self._surface = pg.display.set_mode((1024, 576))
        self._width, self._height = self._surface.get_size()
        self._paused = False
        self._game = MainView(self._surface, self._width, self._height)
        self._view = views["START"](self._surface) # setta view inicial para tela inicial

    def start(self):
        pg.init()
        pg.display.init()
        pg.display.set_caption("Zombie Survival")
        
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

                elif target == "PAUSE":
                    self._paused = True
                    self._view = views["PAUSE"](self._surface)

                elif target in ("RESTART", "PLAY"):
                    self._game = MainView(self._surface, self._width, self._height)
                    self._view = None

                elif target == 'EXIT':
                    self.quit()

            else:
                # view is none
                target = self._game.draw()

                if target == "PAUSE":
                    self._paused = True
                    self._view = views["PAUSE"](self._surface)

    def quit(self):
        exit()

if __name__ == "__main__":
    cleiton = Game()
    cleiton.start()