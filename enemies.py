import pygame
from settings import *
from random import randint
from bullet import Bullet

class Meteor(pygame.sprite.Sprite):
    """Class for Meteors.
    
    Methods:
        destroy(): kill The enemy if it out of screen.
        
        update(): Update over a loop.
    """ 
    def __init__(self,type):
        """Initialize the meteors.

        Args:
            type (1 or 2 or 3 or 4): Change appearance of meteors according to type.
        Attrs:
            rect (pygame rectangle): The rectangle of a meteor.
            
            move_x_pos, move_y_pos (int): Random coordinate to move.
            
            image (file image): The appearance of the meteors.
        """
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
        """Kill the meteor if it out of screen."""
        if self.rect.y >= SCREEN_HEIGHT:
            self.kill()

    def update(self):
        """Update over a loop."""
        self.destroy()
        self.rect.x +=self.move_x_pos
        self.rect.y +=self.move_y_pos

class Enemies(pygame.sprite.Sprite):
    """Class for enemies
    
    Methods: 
        set_cooldown(cooldown): Set the cooldown.
        
        enemy_shoot(): Enemy shoot when this function called.
        
        delay_shoot(): Make the enemy shoot slower.
        
        destroy(): Kill the enemy if it out of screen.
        
        update(self): Update over a loop.
    """
    def __init__(self, type):
        """Initialize a enemy

        Args:
            type (blue or yellow): Change appearance of a enemy according to type.
            
        Attribute:
            image (file image): The image of the enemy.
            
            rect (pygame rectangle): The rectangle of a enemy.
            
            bullets (pygame group): A group of bullets.
            
            ready (boolean): Whether the enemy is ready to shoot.
            
            bullet_time (int): The time at which the enemy shooted.
            
            cooldown (int): The cooldown of a enemy.
        """
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
        """Set the cooldown.

        Args:
            cooldown (int): Value of the cooldown to be set.
        """
        self.cooldown = cooldown
    def enemy_shoot(self):
        """Enemy shoot when this function called."""
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
        """Make the enemy shoot slower."""
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.bullet_time > self.cooldown:
                self.ready = True

    def destroy(self):
        """Kill the enemy if it out of screen."""
        if self.rect.y >= SCREEN_HEIGHT:
            self.kill()

    def update(self):
        """Update over a loop."""
        self.destroy()
        self.enemy_shoot()
        self.bullets.update()
        self.delay_shoot()
        self.rect.y += 2

class Boss(pygame.sprite.Sprite):
    """Class of Boss.
    
    Methods:
        boss_shoot(): When boss ready, shoot.
        
        delay_shoot(): Make boss shoot slower.
        
        boss_movement(self): Boss move.
        
        set_boss_cooldown_health (cooldown,health): Set boss's cooldown and health by arguments.
        
        update(): Update over a loop.
    """
    def __init__(self):
        """Initialize a Boss.
        
        Attributes:
            image (file image): The image of the boss.
            
            rect (pygame rectangle): Rectangle of the boss.
            
            health (int): Boss's health.
            
            bullet (pygame group): Group of bullets.
            
            ready (bool): Boss ready to shoot or not.
            
            bullet_time (int): Set time when boss shoot.
            
            cooldown (int): Boss's cooldown.
            
            speed (int): Boss's speed.
        """
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
        """When boss ready, shoot."""
        if self.ready:
            self.bullets.add(Bullet(self.rect.center, 180))
            self.ready = False
            self.bullet_time = pygame.time.get_ticks()

    def delay_shoot(self):
        """Make boss shoot slower."""
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.bullet_time > self.cooldown:
                self.ready = True

    def boss_movement(self):
        """Boss move."""
        if self.rect.left <= 0 and self.rect.top >= 0:
            self.speed = 5
        elif self.rect.right >= 1280 and self.rect.top >= 0:
            self.speed = -5

    def set_boss_cooldown_health(self,cooldown,health):
        """Set boss's cooldown and health by arguments,

        Args:
            cooldown (int): Cooldown to be set.
            health (int): Health to be set.
        """
        self.cooldown = cooldown
        self.health = health
    
    def update(self):
        """Update over a loop."""
        if self.rect.y >= 0:
            self.rect.x += self.speed
        self.boss_movement()
        self.boss_shoot()
        self.bullets.update()
        self.delay_shoot()
