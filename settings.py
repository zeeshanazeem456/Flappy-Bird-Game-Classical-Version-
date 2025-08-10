import pygame as pg

class Settings:
    def __init__(self):
        pg.init()
        self.FPS = 35
        self.WIDTH = 289
        self.HEIGHT = 511
        self.GAME_SPRITES = {}
        self.GAME_SOUND = {}
        self.pipeVelocity_X = -4
        #player Settings
        self.playerVelocity_Y = -9
        self.playerMaxVelY = 10
        self.playerMinVelY = -8
        self.playerAccY = 1
        self.playerFlapAccv = -10
        self.playerFlapped = False
        self.player = "sprites/bluebird-midflap.png"

    def load_assets(self):
        self.bg = "sprites/background-day.png"
        self.pipe = "sprites/pipe-green.png"
        self.GAME_SPRITES['number'] = (
            pg.image.load("sprites/0.png").convert_alpha(),
            pg.image.load("sprites/1.png").convert_alpha(),
            pg.image.load("sprites/2.png").convert_alpha(),
            pg.image.load("sprites/3.png").convert_alpha(),
            pg.image.load("sprites/4.png").convert_alpha(),
            pg.image.load("sprites/5.png").convert_alpha(),
            pg.image.load("sprites/6.png").convert_alpha(),
            pg.image.load("sprites/7.png").convert_alpha(),
            pg.image.load("sprites/8.png").convert_alpha(),
            pg.image.load("sprites/9.png").convert_alpha(),
        )
        self.GAME_SPRITES['message'] = pg.image.load("sprites/message.png").convert_alpha()
        self.GAME_SPRITES['base'] = pg.image.load("sprites/base.png").convert_alpha()
        self.GAME_SPRITES['pipe'] = (
            pg.transform.rotate(pg.image.load(self.pipe).convert_alpha(),180),
            pg.image.load(self.pipe).convert_alpha()
        )


        #Game Sounds
        self.GAME_SOUND['die'] = pg.mixer.Sound("audio/die.ogg")
        self.GAME_SOUND['hit'] = pg.mixer.Sound("audio/hit.wav")
        self.GAME_SOUND['point'] = pg.mixer.Sound("audio/point.wav")
        self.GAME_SOUND['swoosh'] = pg.mixer.Sound("audio/swoosh.wav")
        self.GAME_SOUND['wing'] = pg.mixer.Sound("audio/wing.wav")

        self.GAME_SPRITES['background'] = pg.image.load(self.bg).convert()
        self.GAME_SPRITES['background_2'] = pg.image.load("sprites/background-night.png").convert()
        self.GAME_SPRITES['Game_Over'] = pg.image.load("sprites/gameover.png").convert_alpha()
        self.GAME_SPRITES['credit'] = pg.image.load("Made-by-Zeeshan-Azeem.png").convert_alpha()
        width, height = self.GAME_SPRITES['credit'].get_size()
        scaled_image = pg.transform.scale(self.GAME_SPRITES['credit'], (width // 4, height // 3))
        self.GAME_SPRITES['credit'] = scaled_image


    def load_player_sprites(self):
        self.GAME_SPRITES['player'] = pg.image.load(self.player).convert_alpha()
        self.GAME_SPRITES['player_1'] = pg.image.load("sprites/bluebird-downflap.png").convert_alpha()
        self.GAME_SPRITES['player_2'] = pg.image.load("sprites/bluebird-upflap.png").convert_alpha()



