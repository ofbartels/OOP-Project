from entities.projectile import Projectile
from entities.towers.defense_towers import DefenseTower
import pygame

class BallistaTower(DefenseTower):
    upgrade_costs = [300, 650, 1000]
    archer_sprite = 'assets/sprites/defense_towers/archer/archer_bullet.png'

    def __init__(self, grid_x, grid_y, building_type='ballista', level=1):
        super().__init__(grid_x, grid_y, building_type, level)
        self.attack_speed = 200
        self.radius = 200
        self.health = self.max_health = 200
        self.last_attack_time = pygame.time.get_ticks()

    def fire(self, enemies):
        nearest_enemy = min(enemies, key=lambda e: self.distance_to(e), default=None)
        if nearest_enemy and self.distance_to(nearest_enemy) < self.radius:
            self.projectiles.append(Projectile((self.world_x, self.world_y), nearest_enemy, 10, 'assets/sprites/defense_towers/archer/arrow.png'))

    def load_sprite(self):
        return super().load_sprite()

    def update(self, current_time, game_context):
        self.combat_update(self, game_context)