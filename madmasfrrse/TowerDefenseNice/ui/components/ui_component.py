# components/ui_component.py
import pygame

class UIComponent:
    def __init__(self, x, y, width, height, image_path=None):
        self.rect = pygame.Rect(x, y, width, height)
        # Load the image only if an image path is provided
        if image_path:
            try:
                self.image = pygame.image.load(image_path)
            except Exception as e:
                print(f"Error loading image at {image_path}: {e}")
                self.image = None
        else:
            self.image = None

    def draw(self, screen):
        if self.image:
            # If an image exists, blit it at the rectangle's top-left corner
            screen.blit(self.image, self.rect.topleft)
        else:
            # Otherwise, draw a default placeholder rectangle
            pygame.draw.rect(screen, (200, 200, 200), self.rect)

    def is_hovered(self, mouse_pos):
        # Return True if the mouse is over the component
        return self.rect.collidepoint(mouse_pos)

    def on_click(self, event):
        # This can be overridden by subclasses to handle click events
        pass
