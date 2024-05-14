import pygame
import math
from .tower_base import Tower
from entities.projectile import Projectile
from entities.soldier import Soldier

class DefenseTower(Tower):
    upgrade_costs = []

    def __init__(self, grid_x, grid_y, building_type, level=1):
        super().__init__(grid_x, grid_y, building_type, level)
        self.attack_speed = 0
        self.last_attack_time = pygame.time.get_ticks()
        self.radius = 0
        self.health = self.max_health = 0
        self.projectiles = []

    def combat_update(self, current_time, game_context):
        if pygame.time.get_ticks() - self.last_attack_time > self.attack_speed:
            self.fire(game_context.enemies)
            self.last_attack_time = pygame.time.get_ticks()
        self.projectiles = [proj for proj in self.projectiles if proj.active]
        for projectile in self.projectiles:
            projectile.update()

    def fire(self, enemies):
        pass

    def distance_to(self, enemy):
        return math.hypot(self.world_x - enemy.world_x, self.world_y - enemy.world_y)

    def draw(self, game_context):
        screen_x, screen_y = game_context.camera.world_to_screen(self.world_x, self.world_y)
        tower_sprite = pygame.transform.flip(self._sprite, self.flipped, False)
        if game_context.camera.zoom < 1:
            tower_sprite = pygame.transform.scale(tower_sprite, (int(tower_sprite.get_width() * game_context.camera.zoom), int(tower_sprite.get_height() * game_context.camera.zoom)))
            game_context.screen.blit(tower_sprite, (screen_x - tower_sprite.get_width() // 2, screen_y - tower_sprite.get_height() // 2 - 10))
        else:
            game_context.screen.blit(tower_sprite, (screen_x - tower_sprite.get_width() // 2, screen_y - tower_sprite.get_height() // 2))
        if self.health < self.max_health:
            self._draw_health_bar(game_context.screen, screen_x, screen_y)
        for projectile in self.projectiles:
            projectile.draw(game_context.screen, game_context.camera)

    def end_of_phase(self):
        self.projectiles.clear()
        self.health = self.max_health

    def upgrade(self):
        if self.level < len(self.upgrade_costs):
            self.level += 1
            self.radius += 100
            self.max_health += 100
            self.attack_speed -= 100
            self.sprite = self.load_sprite()
            self.health = self.max_health
        else:
            print("Maximum level reached.")