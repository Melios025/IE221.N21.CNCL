import pygame
from settings import *
from random import randint
from bullet import Bullet

class Meteor(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 1:
            meteor_1 = pygame.image.load('graphics/meteor_1.png').convert_alpha()
            meteor_1 = pygame.transform.rotozoom(meteor_1,0,0.3)
            self.image = meteor_1
        if type == 2:
            meteor_2 = pygame.image.load('graphics/meteor_2.png').convert_alpha()
            meteor_2 = pygame.transform.rotozoom(meteor_2,0,0.3)
            self.image = meteor_2
        if type == 3:
            meteor_3 = pygame.image.load('graphics/meteor_3.png').convert_alpha()
            meteor_3 = pygame.transform.rotozoom(meteor_3,0,0.3)
            self.image = meteor_3
        if type == 4:
            meteor_4 = pygame.image.load('graphics/meteor_4.png').convert_alpha()
            meteor_4 = pygame.transform.rotozoom(meteor_4,0,0.3)
            self.image = meteor_4
        x_pos = randint(50, 1230)
        y_pos = randint(-50, 0)
        self.move_x_pos = 0
        self.move_y_pos = 0
        while self.move_x_pos == 0:
            self.move_x_pos = randint(-4,4)
        while self.move_y_pos == 0:
            self.move_y_pos = randint(2,4)
        self.rect = self.image.get_rect(center = (x_pos,y_pos))
        
    def destroy(self):
        if self.rect.y >= SCREEN_HEIGHT:
            self.kill()

    def update(self):
        self.destroy()
        self.rect.x +=self.move_x_pos
        self.rect.y +=self.move_y_pos

class Enemies(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.bullets = pygame.sprite.Group()
        self.ready = True
        self.bullet_time = 0
        self.cooldown = ENEMY_COOLDOWN
        self.type = type
        if type == 'blue':
            enemy_blue = pygame.image.load(
                'graphics/enemy1.png').convert_alpha()
            enemy_blue = pygame.transform.rotozoom(enemy_blue, 0, 0.3)
            x_pos = randint(50, 1230)
            y_pos = randint(-100, 0)
            self.image = enemy_blue
        else:
            enemy_yellow = pygame.image.load(
                'graphics/enemy2.png').convert_alpha()
            enemy_yellow = pygame.transform.rotozoom(enemy_yellow, 0, 0.3)
            x_pos = randint(50, 1230)
            y_pos = randint(-100, 0)
            self.image = enemy_yellow
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def set_cooldown(self,cooldown):
        self.cooldown = cooldown
    def enemy_shoot(self):
        if self.ready:
            if self.type == 'blue':
                self.bullets.add(Bullet(self.rect.center, 180))
                self.ready = False
                self.bullet_time = pygame.time.get_ticks()
            else:
                self.bullets.add(Bullet(self.rect.center, -90))
                self.bullets.add(Bullet(self.rect.center, 90))
                self.ready = False
                self.bullet_time = pygame.time.get_ticks()

    def delay_shoot(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.bullet_time > self.cooldown:
                self.ready = True

    def destroy(self):
        if self.rect.y >= SCREEN_HEIGHT:
            self.kill()

    def update(self):
        self.destroy()
        self.enemy_shoot()
        self.bullets.update()
        self.delay_shoot()
        self.rect.y += 2


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/boss.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 1)
        self.rect = self.image.get_rect(midtop=(640, -200))
        self.health = BOSS_HEALTH
        self.bullets = pygame.sprite.Group()
        self.ready = True
        self.bullet_time = 0
        self.cooldown = BOSS_COOLDOWN
        self.speed = 5

    def boss_shoot(self):
        if self.ready:
            self.bullets.add(Bullet(self.rect.center, 180))
            self.ready = False
            self.bullet_time = pygame.time.get_ticks()

    def delay_shoot(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.bullet_time > self.cooldown:
                self.ready = True

    def boss_movement(self):
        if self.rect.left <= 0 and self.rect.top >= 0:
            self.speed = 5
        elif self.rect.right >= 1280 and self.rect.top >= 0:
            self.speed = -5

    def set_boss_cooldown_health(self,cooldown,health):
        self.cooldown = cooldown
        self.health = health
    
    def update(self):
        if self.rect.y >= 0:
            self.rect.x += self.speed
        self.boss_movement()
        self.boss_shoot()
        self.bullets.update()
        self.delay_shoot()
