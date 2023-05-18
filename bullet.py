import pygame
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos,direction):
        super().__init__()
        self.direction = direction
        self.image = pygame.image.load('graphics/bullet.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image,direction,0.5)
        self.rect = self.image.get_rect(center = pos)
    
    def destroy (self):
        if self.rect.y <= -10 or self.rect.y >= SCREEN_HEIGHT:
            self.kill()
    
    def update(self):
        if self.direction == 0:
            self.rect.y -= 6
        elif self.direction == 180:
            self.rect.y += 6
        elif self.direction == 90:
            self.rect.x -= 6
        elif self.direction == -90:
            self.rect.x += 6
        self.destroy()