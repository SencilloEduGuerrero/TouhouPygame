import pygame as pg
import sys, os
from sprites import *
from settings import *


def draw_boss_health(surf, x, y, hbar):
    if hbar < 0:
        hbar = 0
    BAR_LENGTH = 508
    BAR_HEIGHT = 16
    fill = hbar * BAR_LENGTH

    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    col = RED

    BAR_LENGTH2 = 508
    BAR_HEIGHT2 = 12
    fill2 = hbar * BAR_LENGTH2
    fill_rect2 = pg.Rect(x, y + 2, fill2, BAR_HEIGHT2)
    col2 = WHITE

    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, col2, fill_rect2)


def draw_player_health(surf, x, y, hbar):
    if hbar < 0:
        hbar = 0
    BAR_LENGTH = 192
    BAR_HEIGHT = 24
    fill = hbar * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    col = RED

    pg.draw.rect(surf, DARKRED, pg.Rect(576, 140, 192, 24))

    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


def draw_player_power(surf, x, y, hbar):
    if hbar < 0:
        hbar = 0
    BAR_LENGTH = 192
    BAR_HEIGHT = 24
    fill = hbar * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    col = BLUE

    pg.draw.rect(surf, DARKBLUE, pg.Rect(576, 228, 192, 24))

    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


def draw_custom_fonts(surf):
    global PHASE
    global B_SPELL_CARD

    font_path = os.path.join("resources", "Pixel Emulator.otf")
    custom_font = pg.font.Font(font_path, 20)
    custom_fontE = pg.font.Font(font_path, 30)
    custom_fontB = pg.font.Font(font_path, 10)

    extraText = custom_fontE.render("EXTRA", True, (125, 0, 220))
    healthText = custom_font.render("Player Health", True, (255, 255, 255))
    powerText = custom_font.render("Player Power", True, (255, 255, 255))

    bNameText = custom_fontB.render("Komeji Koishi", True, (255, 255, 255))
    bSpellAText = custom_font.render("'Ancestors Standing Beside You'", True, (90, 115, 255))
    bSpellBText = custom_font.render("'Youkai Lazer'", True, (90, 115, 255))
    bSpellCText = custom_font.render("'Subterranean Rose'", True, (90, 115, 255))

    extraTextR = extraText.get_rect()
    healthTextR = healthText.get_rect()
    powerTextR = powerText.get_rect()

    bNameTextR = bNameText.get_rect()
    bSpellATextR = bSpellAText.get_rect()
    bSpellBTextR = bSpellBText.get_rect()
    bSpellCTextR = bSpellCText.get_rect()

    extraTextR.center = (670, 50)
    healthTextR.center = (673, 120)
    powerTextR.center = (673, 210)

    bNameTextR.center = (70, 40)
    bSpellATextR.center = (295, 60)
    bSpellBTextR.center = (390, 60)
    bSpellCTextR.center = (390, 60)

    surf.blit(extraText, extraTextR)
    surf.blit(healthText, healthTextR)
    surf.blit(powerText, powerTextR)

    match PHASE:
        case 0:
            if B_SPELL_CARD:
                surf.blit(bSpellAText, bSpellATextR)
        case 1:
            if B_SPELL_CARD:
                surf.blit(bSpellBText, bSpellBTextR)
        case 2:
            if B_SPELL_CARD:
                surf.blit(bSpellCText, bSpellCTextR)

    if PHASE < 3:
        surf.blit(bNameText, bNameTextR)


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.background = pg.transform.scale(BACKGROUND, (528, 816))
        self.background_position = 0
        self.music_path = os.path.join("audio", "TouhouBossMusic.mp3")
        pg.mixer.music.load(self.music_path)
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(0.2)

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.player_bullets = pg.sprite.Group()
        self.player_special = pg.sprite.Group()
        self.boss_group = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for row in range(17):
            Wall(self, -1, row)
            Wall(self, 11, row)
            if row < 17:
                Wall(self, row, 17)
                Wall(self, row, -1)
        self.player = Player(self, 252, 722)
        self.boss = Boss(self, 245, 96)
        self.boss_group.add(self.boss)
        self.player_group.add(Hitbox(self.player))

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        global B_SPELL_CARD

        self.all_sprites.update()
        self.bullets.update()
        self.player_bullets.update()
        self.player_special.update()
        self.all_sprites.draw(self.screen)

        hits = pg.sprite.groupcollide(self.player_group, self.bullets, False, True)
        for player in hits:
            for bullet in hits[player]:
                self.player.take_damage(5)

        hits = pg.sprite.groupcollide(self.boss_group, self.player_bullets, False, True)
        for boss in hits:
            for bullet in hits[boss]:
                self.boss.take_damage(2)

        hits = pg.sprite.groupcollide(self.boss_group, self.player_special, False, False)
        for boss in hits:
            for bullet in hits[boss]:
                self.boss.take_damage(5)

        if 0 < self.boss.health < 500:
            B_SPELL_CARD = True
        else:
            B_SPELL_CARD = False

    def draw(self):
        global B_SPELL_CARD

        pg.display.set_caption(GAME_NAME + " FPS:({:.0f})".format(self.clock.get_fps()))

        match PHASE:
            case 0:
                self.background_position += 1

                if self.background_position >= self.background.get_height():
                    self.background_position = 0

                self.screen.fill((0, 0, 0))

                self.screen.blit(self.background, (0, self.background_position - self.background.get_height()))
                self.screen.blit(self.background, (0, self.background_position))
            case 1:
                self.background = pg.transform.scale(BACKGROUND_A, (528, 816))

                self.background_position += 5

                if self.background_position >= self.background.get_height():
                    self.background_position = 0

                self.screen.fill((0, 0, 0))

                self.screen.blit(self.background, (0, self.background_position - self.background.get_height()))
                self.screen.blit(self.background, (0, self.background_position))
            case 2:
                self.background = pg.transform.scale(BACKGROUND_B, (528, 816))

                self.background_position += 10

                if self.background_position >= self.background.get_height():
                    self.background_position = 0

                self.screen.fill((0, 0, 0))

                self.screen.blit(self.background, (0, self.background_position - self.background.get_height()))
                self.screen.blit(self.background, (0, self.background_position))
            case 3:
                pg.mixer.music.stop()
                self.screen.fill(BLACK)

        DARK_OVERLAY = pg.Surface((WIDTH_GAME, HEIGHT))
        DARK_OVERLAY.set_alpha(150)
        DARK_OVERLAY.fill((0, 0, 0, 0))

        if B_SPELL_CARD:
            self.screen.blit(DARK_OVERLAY, (0, 0))

        self.player.draw(self.screen)
        self.boss_group.draw(self.screen)
        self.boss.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.screen.blit(HUD, (528, 0))

        pg.draw.line(self.screen, LIGHTGREY, (528, 0), (528, HEIGHT))
        draw_custom_fonts(self.screen)
        draw_player_health(self.screen, 576, 140, self.player.health / PLAYER_HEALTH)
        draw_player_power(self.screen, 576, 228, self.player.special / PLAYER_SPECIAL)
        draw_boss_health(self.screen, 10, 10, self.boss.health / BOSS_HEALTH)

        pg.display.flip()
        self.clock.tick(60)

    def events(self):
        global PHASE
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quit()

        if self.boss.health <= 0:
            PHASE += 1
        if PHASE > 3:
            PHASE = 3


if __name__ == '__main__':
    g = Game()
    while True:
        g.new()
        g.run()
