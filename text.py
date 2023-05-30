import pygame
from settings import *

class Text(pygame.sprite.Sprite):
    """Class for text
    
    Methods:
        destroy(): Kill if not display.
        
        update(): Update over the loop.
    """
    def __init__(self,size,text,color,pos,display=False):
        super().__init__()
        self.display = display
        text_font = pygame.font.Font('font/Pixeltype.ttf', size)
        self.image = text_font.render(f'{text}',False,color)
        self.rect = self.image.get_rect(center=pos)
    
    def destroy(self):
        """Kill if not display."""
        if not self.display:
            self.kill()
    def update(self):
        """Update over the loop"""
        self.destroy()
        self.kill()
        