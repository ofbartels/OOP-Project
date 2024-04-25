import pygame
import random
from ..base_tower import Tower

class SmithTower(Tower):
    def __init__(self, grid_x, grid_y, building_type='smith', level=1):        
        self.color_variants = [
            'supply/Economy/house/blacksmith_blue',
            'supply/Economy/house/blacksmith_green',
            'supply/Economy/house/blacksmith_red',
            'supply/Economy/house/blacksmith_wood',
        ]
        self.building_type = building_type
        self.color_variant = random.choice(self.color_variants)
        super().__init__(grid_x, grid_y, building_type, level)
        self.health = self.max_health = 1000

    def load_sprite(self):
        sprite_path = f"{self.color_variant}({self.level}).png"
        return pygame.image.load(sprite_path).convert_alpha()

    def draw(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
        tower_sprite = self.sprite
        if camera.zoom < 1:
            scaled_width = int(tower_sprite.get_width() * camera.zoom)
            scaled_height = int(tower_sprite.get_height() * camera.zoom)
            scaled_sprite = pygame.transform.scale(tower_sprite, (scaled_width, scaled_height))
            screen.blit(scaled_sprite, (screen_x - scaled_sprite.get_width() // 2, screen_y - scaled_sprite.get_height() // 2 + 10))
        else:
            screen.blit(tower_sprite, (screen_x - tower_sprite.get_width() // 2, screen_y - tower_sprite.get_height() // 2 + 20))
        
        if self.health < self.max_health:
            self.draw_health_bar(screen, screen_x, screen_y,  self.sprite)

    def draw_health_bar(self, screen, screen_x, screen_y, sprite):
        bar_length = 40
        bar_height = 5
        health_ratio = self.health / self.max_health
        fill_length = int(bar_length * health_ratio)
        bar_x = screen_x - bar_length // 2
        bar_y = screen_y - sprite.get_height() // 2 - 10

        pygame.draw.rect(screen, (128, 128, 128), (bar_x, bar_y, bar_length, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_length, bar_height))
        
    def upgrade(self):
        pass