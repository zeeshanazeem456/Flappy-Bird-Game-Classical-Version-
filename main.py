import pygame as pg
from random import randint
import time
import sys
from pygame.locals import *
from settings import Settings
from player import Player

class GameManager:
    def __init__(self):
        self.settings = Settings()
        self.SCREEN = pg.display.set_mode((self.settings.WIDTH,self.settings.HEIGHT))
        self.settings.load_assets()
        self.FPSCLOCK = pg.time.Clock()
        self.player = Player(self.SCREEN)
        self.groundy = self.settings.HEIGHT * 0.8
        self.settings.load_player_sprites()
        self.score = 0
        self.life = 3

    def get_pipe(self):
        pipe_height = self.settings.GAME_SPRITES['pipe'][0].get_height()
        offset = self.settings.HEIGHT / 3
        y2 = offset + randint(0,int(self.settings.HEIGHT - self.settings.GAME_SPRITES['base'].get_height() - 1.2 * offset))
        pipeX = self.settings.WIDTH + 10
        y1 = pipe_height - y2 + offset
        pipe = [
            {'x': pipeX, 'y':-y1},
            {'x': pipeX, 'y': y2}
        ]
        return pipe

    def run(self):
        self.welcome_screen()
        pipe_1 = self.get_pipe()
        pipe_2 = self.get_pipe()
        self.upper_pipe = [
            {'x':self.settings.WIDTH + 200,'y': pipe_1[0]['y']},
            {'x': self.settings.WIDTH + 200 + self.settings.WIDTH/2, 'y':pipe_1[0]['y']}
        ]
        self.lower_pipe = [
            {'x':self.settings.WIDTH + 200,'y': pipe_2[1]['y']},
            {'x': self.settings.WIDTH + 200 + self.settings.WIDTH/2, 'y':pipe_2[1]['y']}
        ]
        self.gameLoop()

    def gameLoop(self):
            while True:
                self.check_events()
                self.update()
                self.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pg.quit()
                sys.exit()
            self.check_keyboard(event)

    def check_keyboard(self,event):
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                if self.player.playerY > 0:
                    self.settings.playerVelocity_Y = self.settings.playerFlapAccv
                    self.settings.playerFlapped = True
                    self.settings.GAME_SOUND['wing'].play()

    def update(self):
        crash_check = self.isCollide(self.player.playerX,self.player.playerY,self.upper_pipe,self.lower_pipe)
        if crash_check:
            self.life -= 1
        if self.life <= 0:
            self.SCREEN.blit(
                self.settings.GAME_SPRITES['Game_Over'],
                (
                    (self.settings.WIDTH - self.settings.GAME_SPRITES['Game_Over'].get_width()) / 2,
                    (self.settings.HEIGHT - self.settings.GAME_SPRITES['Game_Over'].get_height()) / 2
                )
            )
            pg.display.update()
            time.sleep(2)
            self.waiting()
            pg.quit()
            sys.exit()
        playerMidPos = self.player.playerX + self.settings.GAME_SPRITES['player'].get_width() /2
        for pipe in self.upper_pipe:
            pipeMidPos = pipe['x'] + self.settings.GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                self.score = self.score + 1
                #print(f"Your Score is :{self.score}")
                self.settings.GAME_SOUND['point'].play()

        if self.settings.playerVelocity_Y <self.settings.playerMaxVelY and not self.settings.playerFlapped:
            self.settings.playerVelocity_Y += self.settings.playerAccY

        if self.settings.playerFlapped:
            self.settings.playerFlapped = False
        player_height = self.settings.GAME_SPRITES['player'].get_height()
        self.player.playerY = self.player.playerY + min(self.settings.playerVelocity_Y, self.groundy -self.player.playerY - player_height)

        for upperPipe,lowerPipe in zip(self.upper_pipe,self.lower_pipe):
            upperPipe['x'] += self.settings.pipeVelocity_X
            lowerPipe['x'] += self.settings.pipeVelocity_X

        if 0 < self.upper_pipe[0]['x'] < 5:
            newPipe = self.get_pipe()
            self.upper_pipe.append(newPipe[0])
            self.lower_pipe.append(newPipe[1])

        if self.upper_pipe[0]['x'] < -self.settings.GAME_SPRITES['pipe'][0].get_width() :
            self.upper_pipe.pop(0)
            self.lower_pipe.pop(0)
            
    def welcome_screen(self):
        messagex = ((self.settings.WIDTH - self.settings.GAME_SPRITES['message'].get_width())/2)
        messagey = self.settings.HEIGHT * 0.13
        self.basex = 0
        Flag = True
        while Flag:
            for event in pg.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pg.quit()
                    sys.exit()
                elif (event.type == KEYDOWN and event.key == K_SPACE):
                    self.settings.GAME_SOUND['wing'].play()
                    Flag = False
                    break
                else:
                    self.SCREEN.blit(self.settings.GAME_SPRITES['background'],(0,0))
                    self.SCREEN.blit(self.settings.GAME_SPRITES['player'],(self.player.playerX,self.player.playerY))
                    self.SCREEN.blit(self.settings.GAME_SPRITES['message'],(messagex,messagey))
                    self.SCREEN.blit(self.settings.GAME_SPRITES['base'],(self.basex,self.groundy))
                    width = (self.settings.WIDTH - self.settings.GAME_SPRITES['credit'].get_width()) /2
                    height = (self.settings.HEIGHT - self.settings.GAME_SPRITES['credit'].get_height()) /2 + 210
                    self.SCREEN.blit(self.settings.GAME_SPRITES['credit'],(width,self.groundy+6))
                    pg.display.update()
                    pg.display.set_caption(f"FPS: {int(self.FPSCLOCK.get_fps())}")
                    self.FPSCLOCK.tick(self.settings.FPS)

    def draw(self):
        if self.score < 10:
            self.SCREEN.blit(self.settings.GAME_SPRITES['background'],(0,0))
        else:
            self.SCREEN.blit(self.settings.GAME_SPRITES['background_2'],(0,0))
        for upperPipe,lowerPipe in zip(self.upper_pipe,self.lower_pipe):
            self.SCREEN.blit(self.settings.GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
            self.SCREEN.blit(self.settings.GAME_SPRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))
        self.SCREEN.blit(self.settings.GAME_SPRITES['base'],(self.basex,self.groundy))
        rotation_angle = -self.settings.playerVelocity_Y * 3 
        if self.settings.playerVelocity_Y > 2:
            current = self.settings.GAME_SPRITES['player_1']
        elif self.settings.playerVelocity_Y < -2:
            current = self.settings.GAME_SPRITES['player_2']
        else:
            current = self.settings.GAME_SPRITES['player']
        rotated_player = pg.transform.rotate(current, rotation_angle)
        rotated_player = pg.transform.rotozoom(current, rotation_angle, 1)
        #for rotation
        player_rect = rotated_player.get_rect(center=(self.player.playerX + self.settings.GAME_SPRITES['player'].get_width()/2,
                                                    self.player.playerY + self.settings.GAME_SPRITES['player'].get_height()/2))  
        self.SCREEN.blit(rotated_player, player_rect.topleft)
        Digits = [int(x) for x in list(str(self.score))]
        width = 0
        for digit in Digits:
            width += self.settings.GAME_SPRITES['number'][digit].get_width()
        offset_x = (self.settings.WIDTH - width)/ 2
        for digit in Digits:
            self.SCREEN.blit(self.settings.GAME_SPRITES['number'][digit],(offset_x,self.settings.HEIGHT * 0.12))
            offset_x += self.settings.GAME_SPRITES['number'][digit].get_width()
        pg.display.update()
        self.FPSCLOCK.tick(self.settings.FPS)

    def waiting(self):
        waiting_for_input = True
        while waiting_for_input:
            for event in pg.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pg.quit()
                    sys.exit()
                elif event.type == KEYDOWN and (event.key == K_UP or event.key == K_SPACE):
                    waiting_for_input = False
            pg.display.update()
            self.FPSCLOCK.tick(self.settings.FPS)

    def isCollide(self,playerX,playerY,upperpipes,lowerpipes):
        if playerY > self.groundy - 25 or playerY < 0:
            self.settings.GAME_SOUND['hit'].play()
            return True
        for pipe in upperpipes:
            pipeHeight = self.settings.GAME_SPRITES['pipe'][0].get_height()
            if(playerY < pipeHeight + pipe['y'] and abs(playerX - pipe['x']) < self.settings.GAME_SPRITES['pipe'][0].get_width()):
                self.settings.GAME_SOUND['hit'].play()
                return True

        for pipe in lowerpipes:
            if (playerY + self.settings.GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerX - pipe['x']) < self.settings.GAME_SPRITES['pipe'][0].get_width():
                self.settings.GAME_SOUND['hit'].play()
                return True
        return False

if __name__ == "__main__":
    pg.init()
    game = GameManager()
    game.run()

