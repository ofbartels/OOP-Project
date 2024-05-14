from .ui_component import UIComponent
import pygame

class Button(UIComponent):
    def __init__(self, x, y, width, height, text, color, action, resource_manager, image_key=None, font_size=24, visible=True):
        super().__init__(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action
        self.font = pygame.font.Font(None, font_size)  # Load font, adjust path if not using the default
        self.image = resource_manager.get_image(image_key) if image_key else None  # Load image from resource manager
        self.visible = visible  # Control visibility of the button

    def draw(self, screen):
        if not self.visible:  # Only draw the button if it is visible
            return
        
        if self.image:
            # Blit the image to the button's rectangle
            screen.blit(self.image, self.rect)
        else:
            # Draw a rectangle and then render text on it
            pygame.draw.rect(screen, self.color, self.rect)
        
        # Render text over the button
        text_surface = self.font.render(self.text, True, (255, 255, 255))  # Render the text surface
        text_rect = text_surface.get_rect(center=self.rect.center)  # Get the rectangle of the text surface and center it
        screen.blit(text_surface, text_rect)  # Blit the text surface at the centered rect position

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.visible:  # Only handle clicks if the button is visible
                self.action()  # Execute the action if the button is clicked
