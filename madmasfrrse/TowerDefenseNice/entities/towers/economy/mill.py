from entities.towers.economy_tower import EconomyTower
from entities.towers.economy import WheatTower, CornTower
import pygame

class MillTower(EconomyTower):
    upgrade_costs = [400, 600, 800]

    def __init__(self, grid_x, grid_y, building_type='mill', level=1, radius=150, effect_rate=5000):
        super().__init__(grid_x, grid_y, building_type, level)
        self.animation_index = 0
        self.animation_sprites = self.load_animation_sprites()
        self.animation_rate = 300
        self.last_animation_update = pygame.time.get_ticks()
        self.radius = radius
        self.effect_rate = effect_rate
        self.health = self.max_health = 1000

    def load_animation_sprites(self):
        return [
            pygame.image.load('assets/sprites/economy_towers/mill/millpropeller(1).png').convert_alpha(),
            pygame.image.load('assets/sprites/economy_towers/mill/millpropeller(2).png').convert_alpha(),
        ]

    def load_sprite(self):
        sprite_path = self.tower_sprites[self.building_type] + f"({self.level}).png"
        return pygame.image.load(sprite_path).convert_alpha()

    def update(self, current_time, game_context):
        self.update_animation()
        self.update_effect(game_context.towers)

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

    def draw(self, game_context):
        super().draw(game_context)
        self.draw_animation(game_context.screen, game_context.camera)

    def draw_animation(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
        if self.animation_index < len(self.animation_sprites):
            animated_sprite = self.animation_sprites[self.animation_index]
            animated_sprite_scaled = pygame.transform.scale(animated_sprite, (int(animated_sprite.get_width() * camera.zoom), int(animated_sprite.get_height() * camera.zoom)))
            if self.flipped:
                animated_sprite_scaled = pygame.transform.flip(animated_sprite_scaled, True, False)
                screen.blit(animated_sprite_scaled, (screen_x + animated_sprite_scaled.get_width() // 2 - 35, screen_y - animated_sprite_scaled.get_height() // 2 - 10))
            else:
                screen.blit(animated_sprite_scaled, (screen_x - animated_sprite_scaled.get_width() // 2 - 10, screen_y - animated_sprite_scaled.get_height() // 2 - 5))

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