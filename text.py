import pygame
from settings import *

class Text(pygame.sprite.Sprite):
    def __init__(self,size,text,color,pos,display=False):
        super().__init__()
        self.display = display
        text_font = pygame.font.Font('font/Pixeltype.ttf', size)
        self.image = text_font.render(f'{text}',False,color)
        self.rect = self.image.get_rect(center=pos)
    
    def destroy(self):
        if not self.display:
            self.kill()
    def update(self):
        self.destroy()
        self.kill()
        