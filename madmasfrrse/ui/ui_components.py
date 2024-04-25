import pygame

class UIComponent:
    def __init__(self, x, y, width, height, text, color, image_path=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 32)
        self.image = pygame.image.load(image_path) if image_path else None

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def on_click(self, event):
        pass


class TextDisplay(UIComponent):
    def __init__(self, x, y, text, color, background_image=None, font_size=12):
        super().__init__(x, y, 0, 0, text, color)
        self.font = pygame.font.Font(None, font_size)
        self.update_image(background_image)
        self.update()

    def update_image(self, path):
        try:
            if path:
                self.image = pygame.image.load(path).convert_alpha()
            else:
                self.image = None
        except Exception as e:
            print(f"Failed to load image from {path}: {e}")
            self.image = None

    def update(self):
        text_surface = self.font.render(self.text, True, self.color)
        self.width = text_surface.get_width() + 20
        self.height = text_surface.get_height() + 10
        self.rect.size = (self.width, self.height)

    def update_text(self, new_text):
        if self.text != new_text:
            self.text = new_text
            self.update()

    def draw(self, screen):
        if self.image:
            try:
                scaled_image = pygame.transform.scale(self.image, (self.width, self.height))
                screen.blit(scaled_image, (self.rect.x, self.rect.y))
            except Exception as e:
                print(f"Error drawing scaled image: {e}")
        super().draw(screen)


class Button:
    def __init__(self, x, y, width, height, text, color, action, image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action
        self.image = image

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def handle_event(self, event):
        if self.is_clicked(event):
            self.action()
