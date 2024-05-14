# components/text_display.py
import pygame

class TextDisplay:
    def __init__(self, x, y, text, color, font_size):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font_size = font_size
        self.font = pygame.font.SysFont(None, font_size)  # Use default system font
        self.update()

    def update(self):
        """Update the dimensions of the text display based on the text content."""
        self.text_surface = self.font.render(self.text, True, self.color)
        self.rect = self.text_surface.get_rect(topleft=(self.x, self.y))

    def update_text(self, new_text):
        """Update the text displayed and adjust the size accordingly."""
        if self.text != new_text:
            self.text = new_text
            self.update()

    def draw(self, screen):
        """Draw the text display directly on the screen."""
        screen.blit(self.text_surface, self.rect)