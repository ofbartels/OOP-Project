import pygame
from ..base_tower import Tower
from .wheat_tower import WheatTower
from .corn_tower import CornTower

class MillTower(Tower):
    def __init__(self, grid_x, grid_y, building_type='mill', level=1):
        super().__init__(grid_x, grid_y, building_type, level)
        self.animation_index = 0
        self.load_animation_sprites()
        self.radius = 150
        self.effect_rate = 5000
        self.health = self.max_health = 1000

    def load_animation_sprites(self):
        self.animation_sprites = [
            pygame.image.load('supply/Economy/mill/millpropeller(1).png').convert_alpha(),
            pygame.image.load('supply/Economy/mill/millpropeller(2).png').convert_alpha(),
        ]
        self.animation_rate = 300
        self.last_animation_update = pygame.time.get_ticks()

    def update_animation(self):
        if pygame.time.get_ticks() - self.last_animation_update > self.animation_rate:
            self.animation_index = (self.animation_index + 1) % len(self.animation_sprites)
            self.last_animation_update = pygame.time.get_ticks()

    def update_effect(self, towers):
        for tower in towers:
            if isinstance(tower, (WheatTower, CornTower)) and self._is_in_range(tower):
                tower.reduce_level_up_time()

    def _is_in_range(self, other_tower):
        distance = ((self.world_x - other_tower.world_x) ** 2 + (self.world_y - other_tower.world_y) ** 2) ** 0.5
        return distance < self.radius

    def draw(self, screen, camera):
        self.update_animation()
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
        main_sprite = pygame.transform.flip(self.sprite, True, False) if self.flipped else self.sprite
        main_sprite_scaled = pygame.transform.scale(main_sprite, (int(main_sprite.get_width() * camera.zoom), int(main_sprite.get_height() * camera.zoom)))
        screen.blit(main_sprite_scaled, (screen_x - main_sprite_scaled.get_width() // 2, screen_y - main_sprite_scaled.get_height() // 2))
        if self.animation_index < len(self.animation_sprites):
            animated_sprite = self.animation_sprites[self.animation_index]
            animated_sprite_scaled = pygame.transform.scale(animated_sprite, (int(animated_sprite.get_width() * camera.zoom), int(animated_sprite.get_height() * camera.zoom)))
            if self.flipped:
                animated_sprite_scaled = pygame.transform.flip(animated_sprite_scaled, True, False)
                screen.blit(animated_sprite_scaled, (screen_x + animated_sprite_scaled.get_width() // 2 - 35, screen_y - animated_sprite_scaled.get_height() // 2 - 10))
            else:
                screen.blit(animated_sprite_scaled, (screen_x - animated_sprite_scaled.get_width() // 2 - 10, screen_y - animated_sprite_scaled.get_height() // 2 - 5))
        if self.health < self.max_health:
            self.draw_health_bar(screen, screen_x, screen_y, main_sprite)

    def draw_health_bar(self, screen, screen_x, screen_y, sprite):
        bar_length = 40
        bar_height = 5
        health_ratio = self.health / self.max_health
        fill_length = int(bar_length * health_ratio)
        bar_x = screen_x - bar_length // 2
        bar_y = screen_y - sprite.get_height() // 2 - 10
        pygame.draw.rect(screen, (128, 128, 128), (bar_x, bar_y, bar_length, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_length, bar_height))

    upgrade_costs = [400, 600, 800]

    def upgrade(self):
        if self.level < len(self.upgrade_costs):
            self.level += 1
            self.effect_rate += 1000
            self.radius += 100
            self.health += 200
            self.max_health = self.health
            self.sprite = self.load_sprite()
            print(f"Mill upgraded to level {self.level}.")
        else:
            print("Maximum level reached.")
