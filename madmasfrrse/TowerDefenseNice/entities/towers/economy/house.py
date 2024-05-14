from ..tower_base import Tower
import pygame, random
from entities.villager import Villager

class HouseTower(Tower):
    def __init__(self, grid_x, grid_y, building_type='house', level=1):
        self.flipped = False
        self.color_variants = [
            'assets/sprites/economy_towers/house/Blue/wood_blue_house',
            'assets/sprites/economy_towers/house/Green/wood_green_house',
            'assets/sprites/economy_towers/house/Red/wood_red_house',
            'assets/sprites/economy_towers/house/Wood/wood_house',
        ]
        self.building_type = building_type
        self.color_variant = random.choice(self.color_variants)
        super().__init__(grid_x, grid_y, building_type, level)
        self.health = self.max_health = 500
        self.population = 0

    def load_sprite(self):
        sprite_path = f"{self.color_variant}({self.level}).png"
        sprite = pygame.image.load(sprite_path).convert_alpha()
        if self.flipped:
            sprite = pygame.transform.flip(sprite, True, False)
        return sprite
    
    def update(self, current_time, game_context):
        pass

    def scale_sprite(self, sprite, zoom):
        scaled_width = int(sprite.get_width() * zoom)
        scaled_height = int(sprite.get_height() * zoom)
        return pygame.transform.scale(sprite, (scaled_width, scaled_height))

    def draw_scaled_sprite(self, screen, scaled_sprite, screen_x, screen_y):
        screen.blit(scaled_sprite, (screen_x - scaled_sprite.get_width() // 2, screen_y - scaled_sprite.get_height() // 2 + 10))

    def draw_sprite(self, screen, sprite, screen_x, screen_y):
        screen.blit(sprite, (screen_x - sprite.get_width() // 2, screen_y - sprite.get_height() // 2 + 20))

    def check_villagers(self, villagers):
        if self.population == 0:
            self.spawn_person(villagers)
            self.population = 1

    def spawn_person(self, villagers):
        spawn_x = self.world_x + random.randint(-10, 10)
        spawn_y = self.world_y + random.randint(-10, 10)
        new_person = Villager(spawn_x, spawn_y, 'supply/villager.png')
        villagers.append(new_person)