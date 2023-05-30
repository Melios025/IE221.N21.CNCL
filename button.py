import pygame
class Button():
    """Class for a button.
    
    Methods:
        update(screen): Update over the loop and draw the button.
        
        checkForInput(position): Check if the mouse is touch the button.
        
        changeColor(position): Change color when hovered.

    """
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        """Create a Button.

        Args:
            image (string): image to display or none.
            
            pos (tuple): position of the button.
            
            text_input (string): text for button.
            
            font (font): font for the text of the button.
            
            base_color (string): color of the button.
            
            hovering_color (string): color of the button when hovered.
        """
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """Update over the loop and draw the button.

        Args:
            screen (any): Where to draw the button.
        """
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        """Check if the mouse is touch the button.

        Args:
            position (tuple): The position of the mouse.

        Returns:
            _bool_: True if mouse touch the button.
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        """Change color when hovered.

        Args:
            position (tuple): Position of the mouse.
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(
                self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(
                self.text_input, True, self.base_color)
