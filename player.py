import pygame
from bullet import Bullet
from settings import *


class Player(pygame.sprite.Sprite):
    """Class for player.
    
    Methods:
        player_input(): Get user input and shoot.
        
        delay_shoot(): Make player shoot slower.
        
        shoot(): Create a bullet after a shot.
        
        update(): Update over a loop
    """
    def __init__(self):
        """Initialize the player.
        
        Attrs: 
            image (image file): The image of the player 
            
            rect (pygame rectangle): The rectangle of the player
            
            bullets (pygame group): A group of bullets
            
            ready (bool): Whether the player ready to shoot or not
            
            bullet_time (int): The time the player shoot
            
            cooldown (int): The player's cooldown
            
            shoot_sound (sound file): Player's shoot sound
        """
        super().__init__()
        player_surface = pygame.image.load(
            'graphics/player.png').convert_alpha()
        player_surface = pygame.transform.rotozoom(player_surface, 0, 0.8)
        self.image = player_surface
        self.rect = self.image.get_rect(center=(640, 650))
        self.bullets = pygame.sprite.Group()
        self.ready = True
        self.bullet_time = 0
        self.cooldown = PLAYER_COOLDOWN
        self.shoot_sound = pygame.mixer.Sound('audio/shot.mp3')
        self.shoot_sound.set_volume(0.5)

    def player_input(self):
        """Get user input and shoot.
        
        Check if mouse input is left button and call shoot function.
        """
        mouse = pygame.mouse.get_pos()
        mouse_button = pygame.mouse.get_pressed()
        pygame.mouse.set_visible(False)
        if pygame.MOUSEMOTION:
            self.rect = self.image.get_rect(center=(mouse))
        if mouse_button == (1, 0, 0) and self.ready:
            self.shoot()
            self.ready= False
            self.bullet_time = pygame.time.get_ticks()
    
    def delay_shoot(self):
        """Make player shoot slower.
        
        Check if player can shoot after another shot and change player.ready flag.
        """
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.bullet_time >=self.cooldown:
                self.ready = True

    def shoot(self):
        """Create a bullet after a shot.
        
        Add a bullet to the player's bullet sprite group and make sound.
        """
        self.bullets.add(Bullet(self.rect.midtop,0))
        if SOUND ==True:
            self.shoot_sound.play()

    def update(self):
        """Update over a loop"""
        self.player_input()
        self.bullets.update()
        self.delay_shoot()
