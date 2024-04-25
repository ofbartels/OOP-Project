import pygame
from settings import settings
from handlers.state_handler import GameStates

class StartMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.menu_text = 'Press SPACE to Start'
        self.init_menu()

    def init_menu(self):
        self.screen.fill(settings.WHITE)
        text_surface = self.font.render(self.menu_text, True, settings.BLACK)
        text_rect = text_surface.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def handle_event(self, event, state_handler):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                state_handler.change_state(GameStates.BUILD_MODE)

    def draw(self):
        self.screen.fill(settings.WHITE)
        text_surface = self.font.render(self.menu_text, True, settings.BLACK)
        text_rect = text_surface.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2))
        self.screen.blit(text_surface, text_rect)
