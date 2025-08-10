import pygame as pg
from settings import Settings

class Player:
    def __init__(self,screen):
        self.settings = Settings()
        self.screen = screen
        self.playerX = int(self.settings.WIDTH / 5)
        self.settings.load_player_sprites()
        self.playerY = int((self.settings.HEIGHT - self.settings.GAME_SPRITES['player'].get_height()) / 2)
        