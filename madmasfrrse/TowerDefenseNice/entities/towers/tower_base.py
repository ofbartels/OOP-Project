from abc import ABC, abstractmethod
import pygame
from settings import settings

class Tower(ABC):
    tower_sprites = {
        'wheat': 'assets/sprites/economy_towers/wheat/wheat',
        'house': 'assets/sprites/economy_towers/house/Wood/wood_house',
        'smith': 'assets/sprites/economy_towers/blacksmith/blacksmith_blue',
        'corn': 'assets/sprites/economy_towers/corn/corn',
        'mill': 'assets/sprites/economy_towers/mill/mill_blue',
        'archer': 'assets/sprites/defense_towers/archer/archer',
        'barracks': 'assets/sprites/defense_towers/barrack/castle_tower_blue',
        'ballista': 'assets/sprites/defense_towers/barrack/castle_tower_blue',
        'wizard': 'assets/sprites/defense_towers/Wizard/wizard',
    }

    def __init__(self, grid_x, grid_y, building_type, level=1):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.building_type = building_type
        self.level = level
        self.world_x, self.world_y = settings.iso_projection(grid_x, grid_y)
        self._sprite = self.load_sprite()
        self.z_index = self.grid_x + self.grid_y
        self.health = self._max_health = 100
        self.show_edit_buttons = False
        self.flipped = False
        self.mark_for_removal = False

    @abstractmethod
    def load_sprite(self):
        sprite_path = self.tower_sprites[self.building_type] + f"({self.level}).png"
        return pygame.image.load(sprite_path).convert_alpha()
    
    @abstractmethod
    def update(self, current_time, game_context):
        pass
    
    def flip_sprite(self):
        self.flipped = not self.flipped
        self.sprite = self.load_sprite()

    def draw(self, game_context):
        if self.show_edit_buttons:
            self.draw_edit_mode_buttons(game_context)

        screen_x, screen_y = game_context.camera.world_to_screen(self.world_x, self.world_y)
        game_context.screen.blit(self._sprite, (screen_x - self._sprite.get_width() // 2, screen_y - self._sprite.get_height() // 2))
        if self.health < self._max_health:
            self._draw_health_bar(game_context.screen, screen_x, screen_y)

    def _draw_health_bar(self, screen, screen_x, screen_y):
        bar_length = 25
        bar_height = 5
        health_ratio = self.health / self._max_health
        fill_length = int(bar_length * health_ratio)
        bar_x = screen_x - bar_length // 2
        bar_y = screen_y - self._sprite.get_height() // 2 - 10
        pygame.draw.rect(screen, (128, 128, 128), (bar_x, bar_y, bar_length, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_length, bar_height))

    def draw_edit_mode_buttons(self, game_context):
        screen_x, screen_y = game_context.camera.world_to_screen(self.world_x, self.world_y)
        button_width, button_height = 40, 20
        padding = 10

        base_x = screen_x - (2 * button_width + 3 * padding) / 2 - 35
        base_y = screen_y - button_height - padding

        self.delete_button_rect = pygame.Rect(base_x, base_y, button_width, button_height)
        self.left_button_rect = pygame.Rect(base_x + 2 * (button_width + padding), base_y, button_width, button_height)
        self.right_button_rect = pygame.Rect(base_x + 3 * (button_width + padding), base_y, button_width, button_height)

        pygame.draw.rect(game_context.screen, (255, 255, 255), self.delete_button_rect)
        pygame.draw.rect(game_context.screen, (255, 255, 255), self.left_button_rect)
        pygame.draw.rect(game_context.screen, (255, 255, 255), self.right_button_rect)

        font = pygame.font.Font(None, 18)
        delete_text = font.render('Del', True, (0, 0, 0))
        left_text = font.render('<', True, (0, 0, 0))
        right_text = font.render('>', True, (0, 0, 0))
            
        game_context.screen.blit(delete_text, (self.delete_button_rect.x + 10, self.delete_button_rect.y + 3))
        game_context.screen.blit(left_text, (self.left_button_rect.x + 14, self.left_button_rect.y + 3))
        game_context.screen.blit(right_text, (self.right_button_rect.x + 14, self.right_button_rect.y + 3))

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.mark_for_removal = True