import pygame as pg
import os

WIDTH = 816
HEIGHT = 816
WIDTH_GAME = 528
FPS = 60
TILESIZE = 48

GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WHITE = (250, 250, 250)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
DARKRED = (50, 0, 0)
BLUE = (0, 0, 200)
DARKBLUE = (0, 0, 50)

GAME_NAME = 'Touhou Algorithm Genetic'

imagen_path = os.path.join("graphics", "background.png")
BACKGROUND = pg.image.load(imagen_path)
BACKGROUND = pg.transform.scale(BACKGROUND, (528, 816))

imagen_path = os.path.join("graphics", "backgroundA.png")
BACKGROUND_A = pg.image.load(imagen_path)
BACKGROUND_A = pg.transform.scale(BACKGROUND_A, (528, 816))

imagen_path = os.path.join("graphics", "backgroundB.png")
BACKGROUND_B = pg.image.load(imagen_path)
BACKGROUND_B = pg.transform.scale(BACKGROUND_B, (528, 816))

imagen_path = os.path.join("graphics", "NObackground.png")
NO_BACKGROUND = pg.image.load(imagen_path)
NO_BACKGROUND = pg.transform.scale(NO_BACKGROUND, (528, 816))

hud_path = os.path.join("graphics", "Hud.png")
HUD = pg.image.load(hud_path)
HUD = pg.transform.scale(HUD, (288, 816))

PLAYER_SPEED = 600
PLAYER_HEALTH = 100
PLAYER_SPECIAL = 4000

BULLET_SPEED = 1000
BULLET_RATE = 50

SBULLET_SPEED = 500
SBULLET_RATE = 700

BOSS_SPEED = 1000
BOSS_HEALTH = 1000

B_BULLET_SPEED = 150
B_BULLET_RATE = 500
B_BULLET_LIFETIME = 1000

BS_BULLET_SPEED = 50
BS_BULLET_LIFETIME = 2800

S_LAZER_SPEED = 200

MIN_MOVE_INTERVAL = 500
MAX_MOVE_INTERVAL = 1000
MIN_BULLET_INTERVAL = 250
MAX_BULLET_INTERVAL = 500

MIN_BULLET_INTERVAL_S = 2000
MAX_BULLET_INTERVAL_S = 4000

PHASE = 0
B_SPELL_CARD = False