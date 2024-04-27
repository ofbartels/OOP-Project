import pygame, random, math
from ..base_tower import Tower
from ..soldier import Soldier
from .house_tower import HouseTower

class BarrackTower(Tower):
    upgrade_costs = [800, 1200, 2000]
    max_soldiers_per_level = [2, 5, 8]

    def __init__(self, grid_x, grid_y, building_type='barrack', level=1):
        super().__init__(grid_x, grid_y, building_type, level)
        self.spawn_radius = 10
        self.max_soldiers = self.max_soldiers_per_level[level - 1]
        self.health = self.max_health = 1000

    def soldier_update(self, screen, towers, enemies, camera, soldiers):
        house_count = sum(isinstance(tower, HouseTower) for tower in towers)
        self.max_soldiers = min(self.max_soldiers_per_level[self.level - 1], max(1, house_count))

        if len(soldiers) < self.max_soldiers:
            self.spawn_soldier(soldiers, enemies)

        for soldier in soldiers:
            soldier.update()
            soldier.draw(screen, camera)

    def spawn_soldier(self, soldiers, enemies):
        if len(soldiers) < self.max_soldiers:
            angle = random.uniform(0, 2 * math.pi)
            spawn_radius = 50  
            offset_x = spawn_radius * math.cos(angle) - 20
            offset_y = spawn_radius * math.sin(angle) + 50

            new_soldier = Soldier(self.world_x + offset_x, self.world_y + offset_y, soldiers, enemies)
            soldiers.append(new_soldier)
            print(f"Spawned soldier at {self.world_x + offset_x}, {self.world_y + offset_y}")

    def draw(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
        tower_sprite = self.get_scaled_sprite(camera)

        if camera.zoom < 1:
            tower_sprite = pygame.transform.scale(tower_sprite, (int(tower_sprite.get_width() * camera.zoom + 10), int(tower_sprite.get_height() * camera.zoom + 15)))
            screen.blit(tower_sprite, (screen_x - tower_sprite.get_width() // 2, screen_y - tower_sprite.get_height() // 2 - 10))
        
        else: screen.blit(tower_sprite, (screen_x - tower_sprite.get_width() // 2, screen_y - tower_sprite.get_height() // 2))

        if self.health < self.max_health:
            self.draw_health_bar(screen, screen_x, screen_y, tower_sprite)

    def get_scaled_sprite(self, camera):
        if camera.zoom < 1:
            scaled_width = int(self.sprite.get_width() * camera.zoom)
            scaled_height = int(self.sprite.get_height() * camera.zoom)
            return pygame.transform.scale(self.sprite, (scaled_width, scaled_height))
        return self.sprite

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
        if self.level < len(self.upgrade_costs):
            self.level += 1
            self.max_soldiers = self.max_soldiers_per_level[self.level - 1]
            self.health += 100
            self.max_health = self.health
            self.sprite = self.load_sprite()
            print(f"Barrack Tower upgraded to level {self.level}. Max soldiers: {self.max_soldiers}")
        else:
            print("Maximum level reached.")
