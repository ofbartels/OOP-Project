import pygame
import math
from ..base_tower import Tower
from entities.projectile import Projectile

class ArcherTower(Tower):
    upgrade_costs = [300, 650, 1000]

    def __init__(self, grid_x, grid_y, building_type='archer', level=1):
        super().__init__(grid_x, grid_y, building_type, level)
        self.attack_speed = 500
        self.last_attack_time = pygame.time.get_ticks()
        self.radius = 200
        self.health = self.max_health = 200
        self.projectiles = []

    def combat_update(self, current_time, towers, enemies, camera):
        if pygame.time.get_ticks() - self.last_attack_time > self.attack_speed:
            self.fire(enemies)
            self.last_attack_time = pygame.time.get_ticks()
        self.projectiles = [proj for proj in self.projectiles if proj.active]
        for projectile in self.projectiles:
            projectile.update()

    def fire(self, enemies):
        nearest_enemy = min(enemies, key=lambda e: self.distance_to(e), default=None)
        if nearest_enemy and self.distance_to(nearest_enemy) < self.radius:
            self.projectiles.append(Projectile((self.world_x, self.world_y), nearest_enemy, 10))

    def distance_to(self, enemy):
        return math.hypot(self.world_x - enemy.world_x, self.world_y - enemy.world_y)

    def draw(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
        tower_sprite = pygame.transform.flip(self.sprite, self.flipped, False)
        
        if camera.zoom < 1:
            tower_sprite = pygame.transform.scale(tower_sprite, (int(tower_sprite.get_width() * camera.zoom), int(tower_sprite.get_height() * camera.zoom)))
            screen.blit(tower_sprite, (screen_x - tower_sprite.get_width() // 2, screen_y - tower_sprite.get_height() // 2 - 10))
        
        else: screen.blit(tower_sprite, (screen_x - tower_sprite.get_width() // 2, screen_y - tower_sprite.get_height() // 2))

        if self.health < self.max_health:
            self.draw_health_bar(screen, screen_x, screen_y, tower_sprite)

        for projectile in self.projectiles:
            projectile.draw(screen, camera)

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
