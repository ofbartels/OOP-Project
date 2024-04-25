import pygame
from ..base_tower import Tower
from entities.projectile import Projectile
from handlers.state_handler import GameStates

class ArcherTower(Tower):
    def __init__(self, grid_x, grid_y, building_type='archer', level=1):
        super().__init__(grid_x, grid_y, building_type, level)
        self.attack_speed = 500
        self.last_attack_time = pygame.time.get_ticks()
        self.radius = 200
        self.health = self.max_health = 1000
        self.projectiles = []

    def combat_update(self, current_time, towers, enemies, camera):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > self.attack_speed:
            self.fire(enemies)
            self.last_attack_time = current_time
        self.projectiles = [proj for proj in self.projectiles if proj.active]
        for projectile in self.projectiles:
            projectile.update()

    def fire(self, enemies):
        nearest_enemy = None
        min_distance = float('inf')
        for enemy in enemies:
            distance = ((self.world_x - enemy.world_x) ** 2 + (self.world_y - enemy.world_y) ** 2) ** 0.5
            if distance < self.radius and distance < min_distance:
                min_distance = distance
                nearest_enemy = enemy
        if nearest_enemy:
            projectile = Projectile((self.world_x, self.world_y), nearest_enemy, 10)
            self.projectiles.append(projectile)


    def draw_health_bar(self, screen, screen_x, screen_y, sprite):
        bar_length = 40
        bar_height = 5
        health_ratio = self.health / self.max_health
        fill_length = int(bar_length * health_ratio)
        bar_x = screen_x - bar_length // 2
        bar_y = screen_y - sprite.get_height() // 2 - 10

        pygame.draw.rect(screen, (128, 128, 128), (bar_x, bar_y, bar_length, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_length, bar_height))

    upgrade_costs = [200, 300, 500, 800, 1200]
    def draw(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)

        if self.flipped:
            tower_sprite = pygame.transform.flip(self.sprite, True, False)
        else:
            tower_sprite = self.sprite

        screen.blit(tower_sprite, (screen_x - tower_sprite.get_width() // 2, screen_y - tower_sprite.get_height() // 2))
        
        for projectile in self.projectiles:
                projectile.draw(screen, camera)
        if self.health < self.max_health:
            self.draw_health_bar(screen, screen_x, screen_y, self.sprite)

    def upgrade(self):
        if self.level < len(self.upgrade_costs):
            self.level += 1
            self.max_health += 200
            self.health = self.max_health
            self.attack_speed -= 50
            self.sprite = self.load_sprite()
            print(f"Archer Tower upgraded to level {self.level}. Health: {self.max_health}, Attack Speed: {self.attack_speed}")
        else:
            print("Maximum level reached.")