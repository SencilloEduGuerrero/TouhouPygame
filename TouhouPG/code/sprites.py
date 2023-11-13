import os
import pygame as pg
import math
import random
from settings import *

vec = pg.math.Vector2


class Hitbox(pg.sprite.Sprite):
    def __init__(self, player):
        super().__init__(player.game.all_sprites)
        self.player = player
        hitbox_path = os.path.join("graphics", "R_Hitbox.png")
        self.image = pg.image.load(hitbox_path)
        self.image = pg.transform.scale(self.image, (8, 8))
        self.rect = self.image.get_rect()

    def update(self):
        if self.player.player_alive:
            self.rect.center = self.player.rect.center
        else:
            self.kill()


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.imagen_path = os.path.join("graphics", "R_Base.png")
        self.image = pg.image.load(self.imagen_path)
        self.image = pg.transform.scale(self.image, (24, 48))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.pos = vec(x, y)
        self.last_shot = 0
        self.last_shotS = 0
        self.player_alive = True
        self.health = PLAYER_HEALTH
        self.special = PLAYER_SPECIAL

        self.decoration_path = os.path.join("graphics", "R_Spell.png")
        self.decoration_image = pg.image.load(self.decoration_path)
        self.decoration_image = pg.transform.scale(self.decoration_image, (48, 48))
        self.decoration_rect = self.decoration_image.get_rect()
        self.decoration_offset = (0, 0)

        self.hitbox = Hitbox(self)

    SPECIAL_REGEN_RATE = 10

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED

        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shotS > BULLET_RATE:
                self.last_shotS = now
                self.bullets_attack()

        if self.special >= 1000:
            if keys[pg.K_z]:
                now = pg.time.get_ticks()
                if now - self.last_shot > SBULLET_RATE:
                    self.last_shot = now
                    self.special -= 1000
                    self.bullets_special()
            else:
                self.special += Player.SPECIAL_REGEN_RATE
        else:
            self.special += Player.SPECIAL_REGEN_RATE

        self.special = min(PLAYER_SPECIAL, self.special)

    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy
            self.pos = vec(self.x, self.y)

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def bullets_attack(self):
        attack = pg.mixer.Sound(os.path.join('audio', 'damage00.wav'))
        attack.set_volume(0.3)
        pg.mixer.Sound.play(attack)

        bullet1 = BulletCard(self.game, self.pos)
        bullet2 = BulletCard(self.game, self.pos + vec(24, 0))

    def bullets_special(self):
        special = pg.mixer.Sound(os.path.join('audio', 'power1.wav'))
        special.set_volume(0.3)
        pg.mixer.Sound.play(special)

        bulletA = BulletSpecial(self.game, self.pos + vec(-35, 22))
        bulletB = BulletSpecial(self.game, self.pos + vec(60, 22))
        bulletC = BulletSpecial(self.game, self.pos + vec(12, 70))
        bulletD = BulletSpecial(self.game, self.pos + vec(12, -25))

        bulletA = BulletSpecialMini(self.game, self.pos + vec(-35, -25))
        bulletB = BulletSpecialMini(self.game, self.pos + vec(60, -25))
        bulletC = BulletSpecialMini(self.game, self.pos + vec(-35, 70))
        bulletD = BulletSpecialMini(self.game, self.pos + vec(60, 70))

    def update(self):
        if self.player_alive:
            self.get_keys()
            self.x += self.vx * self.game.dt
            self.y += self.vy * self.game.dt
            self.x = int(self.x)
            self.y = int(self.y)

            self.rect.x = self.x
            self.collide_with_walls('x')
            self.rect.y = self.y
            self.collide_with_walls('y')
            self.pos = vec(self.x, self.y)

            self.hitbox.update()

            self.decoration_rect.center = (self.rect.centerx + self.decoration_offset[0],
                                           self.rect.centery + self.decoration_offset[1])

            if self.health <= 0:
                self.player_defeated()

    def take_damage(self, damage):
        special = pg.mixer.Sound(os.path.join('audio', 'timeout.wav'))
        special.set_volume(0.5)
        pg.mixer.Sound.play(special)

        if self.player_alive:
            self.health -= damage
            if self.health <= 0:
                self.player_defeated()

    def player_defeated(self):
        special = pg.mixer.Sound(os.path.join('audio', 'pldead00.wav'))
        special.set_volume(0.1)
        pg.mixer.Sound.play(special)

        self.player_alive = False
        self.kill()

    def draw(self, surf):
        if self.player_alive:
            surf.blit(self.decoration_image, self.decoration_rect.topleft)
            surf.blit(self.image, self.rect.topleft)


class BulletCard(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.player_bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        bulletc_path = os.path.join("graphics", "R_Shots_A.png")
        self.image = pg.image.load(bulletc_path)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = vec(0, -BULLET_SPEED)
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if self.rect.bottom < 0:
            self.kill()


class BulletSpecial(pg.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.all_sprites, game.player_special)
        self.game = game

        self.colors = ["R_Special_RA.png", "R_Special_GA.png", "R_Special_BA.png"]
        color_index = random.randint(0, 2)
        bullets_path = os.path.join("graphics", self.colors[color_index])

        self.original_image = pg.image.load(bullets_path)
        self.original_image = pg.transform.scale(self.original_image, (48, 48))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = vec(0, -SBULLET_SPEED)
        self.spawn_time = pg.time.get_ticks()
        self.delay = 500

    def update(self):
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.spawn_time

        if elapsed_time >= self.delay:
            self.pos += self.vel * self.game.dt
            self.rect.center = self.pos

            if self.pos.y <= 0:
                bounce = pg.mixer.Sound(os.path.join('audio', 'tan00.wav'))
                pg.mixer.Sound.play(bounce)
                bounce.set_volume(0.1)
                self.vel.y = SBULLET_SPEED

            self.pos += self.vel * self.game.dt
            self.rect.center = self.pos

            if self.rect.top > HEIGHT:
                self.kill()


class BulletSpecialMini(pg.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.all_sprites, game.player_bullets)
        self.game = game

        self.colors = ["R_Special_RB.png", "R_Special_GB.png", "R_Special_BB.png"]
        color_index = random.randint(0, 2)
        bullets_path = os.path.join("graphics", self.colors[color_index])

        self.original_image = pg.image.load(bullets_path)
        self.original_image = pg.transform.scale(self.original_image, (32, 32))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = vec(0, -SBULLET_SPEED)
        self.spawn_time = pg.time.get_ticks()
        self.delay = 500

    def update(self):
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.spawn_time

        if elapsed_time >= self.delay:
            self.pos += self.vel * self.game.dt
            self.rect.center = self.pos
            self.rect.center = (self.pos.x, self.pos.y)


class Boss(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.imagen_path = os.path.join("graphics", "K_Base.png")
        self.image = pg.image.load(self.imagen_path)
        self.image = pg.transform.scale(self.image, (38, 54))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.pos = vec(self.x, self.y)
        self.vel = vec(0, 0)
        self.last_move_time = pg.time.get_ticks()
        self.move_interval = random.randint(1000, 3000)
        self.target_x = 0
        self.target_y = 0
        self.first_step = False
        self.boss_alive = True
        self.health = BOSS_HEALTH
        self.berserk = B_SPELL_CARD
        self.last_shot = 0
        self.bullet_spiral_timer = 0
        self.next_bullet_spiral_time = self.get_next_bullet_spiral_time()
        self.next_bullet_spiral_time_2 = self.get_next_bullet_spiral_time_2()
        self.bullet_special_timer = 0
        self.next_bullet_special_time = self.get_next_bullet_special_time()
        self.line_attack = False

        self.decoration_path = os.path.join("graphics", "K_Spell.png")
        self.decoration_image = pg.image.load(self.decoration_path)
        self.decoration_image = pg.transform.scale(self.decoration_image, (128, 128))
        self.decoration_rect = self.decoration_image.get_rect()
        self.decoration_offset = (0, 0)

    @staticmethod
    def get_next_bullet_spiral_time():
        return pg.time.get_ticks() + random.randint(MIN_BULLET_INTERVAL, MAX_BULLET_INTERVAL)

    @staticmethod
    def get_next_bullet_spiral_time_2():
        return pg.time.get_ticks() + random.randint(MIN_BULLET_INTERVAL * 3, MAX_BULLET_INTERVAL * 3)

    @staticmethod
    def get_next_bullet_special_time():
        return pg.time.get_ticks() + random.randint(MIN_BULLET_INTERVAL_S, MAX_BULLET_INTERVAL_S)

    def set_new_move_interval(self):
        self.move_interval = random.randint(MIN_MOVE_INTERVAL, MAX_MOVE_INTERVAL)
        self.target_x = random.randint(0, WIDTH_GAME - self.rect.width)
        self.target_y = random.randint(48, HEIGHT / 4 - self.rect.height)

    def update(self):
        global PHASE
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.last_move_time

        if self.boss_alive:
            match PHASE:
                case 0:
                    if self.health >= 500:
                        if current_time >= self.next_bullet_spiral_time:
                            self.boss_bullets_attack()
                            self.next_bullet_spiral_time = self.get_next_bullet_spiral_time()
                    elif 0 < self.health < 500:
                        if not self.berserk:
                            self.spell_card()

                        if current_time >= self.next_bullet_special_time:
                            self.boss_bullets_special(num_bullets=9)
                            self.next_bullet_special_time = self.get_next_bullet_special_time()
                    else:
                        self.back_normality()
                        PHASE += 1
                        self.health = 1000
                case 1:
                    if self.health >= 500:
                        if current_time >= self.next_bullet_spiral_time:
                            self.boss_bullets_attack_2()
                            self.next_bullet_spiral_time = self.get_next_bullet_spiral_time()
                    elif 0 < self.health < 500:
                        if not self.berserk:
                            self.spell_card()

                        if current_time >= self.next_bullet_special_time:
                            self.boss_bullets_special_2()
                            self.next_bullet_special_time = self.get_next_bullet_special_time()
                    else:
                        self.back_normality()
                        PHASE += 1
                        self.health = 1000
                case 2:
                    if self.health >= 500:
                        if current_time >= self.next_bullet_spiral_time_2:
                            self.boss_bullets_attack_3()
                            self.next_bullet_spiral_time_2 = self.get_next_bullet_spiral_time_2()
                    elif 0 < self.health < 500:
                        if not self.berserk:
                            self.line_attack = False
                            self.spell_card()

                        if current_time >= self.next_bullet_special_time:
                            self.boss_bullets_special_3()
                            self.next_bullet_special_time = self.get_next_bullet_special_time()
                    else:
                        PHASE += 1
                        self.boss_defeated()

            if elapsed_time >= self.move_interval:
                self.set_new_move_interval()
                self.last_move_time = current_time
                if not self.first_step:
                    self.first_step = True
            else:
                self.move_interval = random.randint(4000, 8000)

            if self.first_step:
                interp_factor = 0.1
                self.pos.x = pg.math.lerp(self.pos.x, self.target_x, interp_factor)
                self.pos.y = pg.math.lerp(self.pos.y, self.target_y, interp_factor)

                self.pos.x = max(0, min(int(self.pos.x), WIDTH_GAME - self.rect.width))
                self.pos.y = max(48, min(int(self.pos.y), HEIGHT / 4 - self.rect.height))

                self.rect.topleft = int(self.pos.x), int(self.pos.y)
            else:
                interp_factor = 0.1
                self.pos.x = pg.math.lerp(self.pos.x, self.target_x, interp_factor)
                self.pos.y = pg.math.lerp(self.pos.y, self.target_y, interp_factor)

                self.pos.x = max(245, min(int(self.pos.x), WIDTH_GAME - self.rect.width))
                self.pos.y = max(96, min(int(self.pos.y), HEIGHT / 4 - self.rect.height))

                self.rect.topleft = self.pos.x, self.pos.y

    def boss_bullets_attack(self):
        attack = pg.mixer.Sound(os.path.join('audio', 'tan02.wav'))
        attack.set_volume(0.2)
        pg.mixer.Sound.play(attack)

        bullet1 = BulletSpiral(self.game, self.rect.center)
        self.game.bullets.add(bullet1)

    def boss_bullets_attack_2(self):
        attack = pg.mixer.Sound(os.path.join('audio', 'tan01.wav'))
        attack.set_volume(0.2)
        pg.mixer.Sound.play(attack)

        bullet1 = BulletSpam(self.game, self.rect.center + vec(64, 0))
        bullet2 = BulletSpam(self.game, self.rect.center + vec(-64, 0))
        self.game.bullets.add(bullet1)
        self.game.bullets.add(bullet2)

    def boss_bullets_attack_3(self):
        attack = pg.mixer.Sound(os.path.join('audio', 'plst00.wav'))
        attack.set_volume(0.2)
        pg.mixer.Sound.play(attack)

        for i in range(9):
            bullet1 = BulletFall(self.game, vec(64 * i, 96))
            self.game.bullets.add(bullet1)

    def spell_card(self):
        special = pg.mixer.Sound(os.path.join('audio', 'cat00.wav'))
        special.set_volume(0.3)
        pg.mixer.Sound.play(special)

        self.berserk = True

    def back_normality(self):
        special = pg.mixer.Sound(os.path.join('audio', 'enep00.wav'))
        special.set_volume(0.3)
        pg.mixer.Sound.play(special)

        self.berserk = False

    def take_damage(self, damage):
        special = pg.mixer.Sound(os.path.join('audio', 'item00.wav'))
        special.set_volume(0.05)
        pg.mixer.Sound.play(special)

        if self.boss_alive:
            self.health -= damage
            if self.health <= 0 and PHASE == 3:
                self.boss_defeated()

    def boss_defeated(self):
        special = pg.mixer.Sound(os.path.join('audio', 'enep01.wav'))
        special.set_volume(0.1)
        pg.mixer.Sound.play(special)

        self.berserk = False
        self.boss_alive = False
        self.kill()

    def boss_bullets_special(self, num_bullets):
        attack = pg.mixer.Sound(os.path.join('audio', 'lazer00.wav'))
        attack.set_volume(0.05)
        pg.mixer.Sound.play(attack)

        for i in range(num_bullets):
            if 0 < num_bullets:
                num_bullets = 6
                bullet1 = BulletDiamondV(self.game, vec(96 * i, HEIGHT))
                self.game.bullets.add(bullet1)

            bullet2 = BulletDiamondH(self.game, vec(WIDTH_GAME, 96 * i))
            self.game.bullets.add(bullet2)

    def boss_bullets_special_2(self):
        attack = pg.mixer.Sound(os.path.join('audio', 'gun00.wav'))
        attack.set_volume(0.5)
        pg.mixer.Sound.play(attack)

        charge = BulletCharge(self.game, self.rect.center)

    def boss_bullets_special_3(self):
        attack = pg.mixer.Sound(os.path.join('audio', 'lazer01.wav'))
        attack.set_volume(0.5)
        pg.mixer.Sound.play(attack)

        MIN_SEPARATION = 48
        flower_positions = set()

        def generate_random_flower_position():
            while True:
                x = random.randint(0, WIDTH_GAME - 12)
                if all(abs(x - pos) >= MIN_SEPARATION for pos in flower_positions):
                    flower_positions.add(x)
                    return x

        S_SEED_SPAWN_1 = generate_random_flower_position()
        S_SEED_SPAWN_2 = generate_random_flower_position()
        S_SEED_SPAWN_3 = generate_random_flower_position()
        S_SEED_SPAWN_4 = generate_random_flower_position()
        S_SEED_SPAWN_5 = generate_random_flower_position()

        flower1 = BulletFlower(self.game, vec(S_SEED_SPAWN_1, self.pos.y))
        flower2 = BulletFlower(self.game, vec(S_SEED_SPAWN_2, self.pos.y))
        flower3 = BulletFlower(self.game, vec(S_SEED_SPAWN_3, self.pos.y))
        flower4 = BulletFlower(self.game, vec(S_SEED_SPAWN_4, self.pos.y))
        flower5 = BulletFlower(self.game, vec(S_SEED_SPAWN_5, self.pos.y))

    def draw(self, surf):
        if self.berserk:
            self.decoration_rect.center = (self.rect.centerx + self.decoration_offset[0], self.rect.centery + self.decoration_offset[1])

            surf.blit(self.decoration_image, self.decoration_rect.topleft)
            surf.blit(self.image, self.rect.topleft)


class BulletSpiral(pg.sprite.Sprite):
    def __init__(self, game, boss_pos):
        super().__init__()
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        bulletb_path = os.path.join("graphics", "K_Shots_A.png")
        self.image = pg.image.load(bulletb_path)
        self.rect = self.image.get_rect()
        self.pos = vec(boss_pos)
        self.rect.center = boss_pos
        self.angle = 0
        self.radius = 2
        self.angular_speed = 2
        self.speed = B_BULLET_SPEED

    def update(self):
        self.angle += self.angular_speed * self.game.dt

        self.pos.x = self.rect.centerx + math.cos(self.angle) * self.radius
        self.pos.y = self.rect.centery + math.sin(self.angle) * self.radius

        self.pos.y += self.speed * self.game.dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        if self.rect.top < 0:
            self.kill()


class BulletDiamondV(pg.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.all_sprites, game.bullets)
        self.game = game
        bullets_path = os.path.join("graphics", "K_Special_A.png")
        self.original_image = pg.image.load(bullets_path)
        self.original_image = pg.transform.scale(self.original_image, (24, 48))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = vec(0, -BS_BULLET_SPEED)
        self.spawn_time = pg.time.get_ticks()
        self.delay = 500

    def update(self):
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.spawn_time

        if elapsed_time >= self.delay:
            self.pos.y += self.vel.y * self.game.dt
            self.rect.center = self.pos

            if self.pos.y <= 0:
                bounce = pg.mixer.Sound(os.path.join('audio', 'tan00.wav'))
                pg.mixer.Sound.play(bounce)
                bounce.set_volume(0.1)
                self.vel.y = BS_BULLET_SPEED

            self.pos.y += self.vel.y * self.game.dt
            self.rect.center = self.pos

            if self.rect.top > HEIGHT:
                self.kill()


class BulletDiamondH(pg.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.all_sprites, game.bullets)
        self.game = game
        bullets_path = os.path.join("graphics", "K_SPECIAL_B.png")
        self.original_image = pg.image.load(bullets_path)
        self.original_image = pg.transform.scale(self.original_image, (48, 24))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = vec(-BS_BULLET_SPEED, 0)
        self.spawn_time = pg.time.get_ticks()
        self.delay = 500

    def update(self):
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.spawn_time

        if elapsed_time >= self.delay:
            self.pos += self.vel * self.game.dt
            self.rect.center = self.pos

            if self.pos.x <= 0:
                bounce = pg.mixer.Sound(os.path.join('audio', 'tan00.wav'))
                pg.mixer.Sound.play(bounce)
                bounce.set_volume(0.1)
                self.vel.x = BS_BULLET_SPEED

            self.pos += self.vel * self.game.dt
            self.rect.center = self.pos

            if self.rect.left > WIDTH_GAME:
                self.kill()


class BulletSpam(pg.sprite.Sprite):
    def __init__(self, game, boss_pos):
        super().__init__(game.all_sprites, game.bullets)
        self.game = game
        bulletb_path = os.path.join("graphics", "K_Shots_B.png")
        self.image = pg.image.load(bulletb_path)
        self.rect = self.image.get_rect()
        self.pos = vec(boss_pos)
        self.rect.center = boss_pos
        self.angle = 5
        self.radius = 2
        self.angular_speed = 5
        self.speed = B_BULLET_SPEED / 20
        self.timer = pg.time.get_ticks()
        self.timer_delay = 1800

    def update(self):
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.timer

        self.angle += self.angular_speed * self.game.dt

        self.pos.x = self.rect.centerx + math.cos(self.angle) * self.radius
        self.pos.y = self.rect.centery + math.sin(self.angle) * self.radius

        if elapsed_time >= self.timer_delay:
            self.angular_speed = 0
            self.speed = B_BULLET_SPEED

        self.rect.center = (round(self.pos.x), round(self.pos.y))

        if self.rect.top < 0:
            self.kill()


class BulletCharge(pg.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.all_sprites, game.bullets)
        self.game = game
        bullets_path = os.path.join("graphics", "K_Lazer_A.png")
        self.original_image = pg.image.load(bullets_path)
        self.original_image = pg.transform.scale(self.original_image, (96, 96))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = vec(0, 0)
        self.spawn_time = pg.time.get_ticks()
        self.delay = 1500
        self.lifetime = BS_BULLET_LIFETIME
        self.sound_played = False

    def update(self):
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.spawn_time

        if elapsed_time >= self.delay and not self.sound_played:
            lazer = pg.mixer.Sound(os.path.join('audio', 'nep00.wav'))
            pg.mixer.Sound.play(lazer)
            lazer.set_volume(0.5)
            self.sound_played = True

            lazer = BulletLazer(self.game, self.rect.center + vec(0, 96))
            self.spawn_time = current_time

        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        if current_time - self.spawn_time >= self.lifetime:
            self.kill()


class BulletLazer(pg.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.all_sprites, game.bullets)
        self.game = game
        bullets_path = os.path.join("graphics", "K_Lazer_B.png")
        self.original_image = pg.image.load(bullets_path)
        self.original_image = pg.transform.scale(self.original_image, (96, 256))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = vec(0, S_LAZER_SPEED)
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        if self.rect.top > HEIGHT:
            self.kill()


class BulletLine(pg.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.all_sprites)
        self.game = game
        bullets_path = os.path.join("graphics", "K_Line.png")
        self.original_image = pg.image.load(bullets_path)
        self.original_image = pg.transform.scale(self.original_image, (WIDTH_GAME, 16))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = vec(0, 0)
        self.spawn_time = pg.time.get_ticks()
        self.first_set_delay = 500
        self.second_set_delay = 750
        self.spawned_first_set = False

    def update(self):
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.spawn_time

        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos


class BulletFall(pg.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.all_sprites)
        self.game = game
        bullets_path = os.path.join("graphics", "K_Shots_C.png")
        self.original_image = pg.image.load(bullets_path)
        self.original_image = pg.transform.scale(self.original_image, (24, 48))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = vec(0, BULLET_SPEED / 10)
        self.spawn_time = pg.time.get_ticks()
        self.delay = 500

    def update(self):
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.spawn_time

        if elapsed_time >= self.delay:
            self.pos += self.vel * self.game.dt
            self.rect.center = self.pos

        if self.rect.top > HEIGHT:
            self.kill()


class BulletFlower(pg.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.all_sprites, game.bullets)
        self.game = game
        bullets_path = os.path.join("graphics", "K_Seed.png")
        self.original_image = pg.image.load(bullets_path)
        self.original_image = pg.transform.scale(self.original_image, (24, 24))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = vec(0, -BS_BULLET_SPEED)
        self.spawn_time = pg.time.get_ticks()
        self.delay = 500
        self.bounce_count = 0

    def update(self):
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.spawn_time

        if elapsed_time >= self.delay:
            self.pos.y += self.vel.y * self.game.dt
            self.rect.center = self.pos

            if self.pos.y <= 0 and self.bounce_count == 0:
                self.bounce_count += 1
                self.vel.y = B_BULLET_SPEED * 2

                bounce = pg.mixer.Sound(os.path.join('audio', 'powerup.wav'))
                pg.mixer.Sound.play(bounce)
                bounce.set_volume(0.1)

            if self.pos.y >= HEIGHT and self.bounce_count == 1:
                bullets_path = os.path.join("graphics", "K_Flower.png")
                self.original_image = pg.image.load(bullets_path)
                self.original_image = pg.transform.scale(self.original_image, (64, 64))
                self.image = self.original_image
                self.rect = self.image.get_rect()

                self.bounce_count += 1
                self.vel.y = -B_BULLET_SPEED / 2

                bounce = pg.mixer.Sound(os.path.join('audio', 'ok00.wav'))
                pg.mixer.Sound.play(bounce)
                bounce.set_volume(0.1)

            self.pos.y += self.vel.y * self.game.dt
            self.rect.center = self.pos

            if self.rect.top > HEIGHT:
                self.kill()


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
