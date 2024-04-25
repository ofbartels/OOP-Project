from ..base_tower import Tower
from ..soldier import Soldier
from .house_tower import HouseTower
import math, pygame

class BarrackTower(Tower):
    def __init__(self, grid_x, grid_y, building_type='barrack', level=1):
        super().__init__(grid_x, grid_y, building_type, level)
        self.spawn_radius = 50 
        self.max_soldiers = 1
        self.health = self.max_health = 1000
    
    upgrade_costs = [300, 400, 600]

    def combat_update(self, current_time, towers, enemies, camera, soldiers):
        house_count = sum(1 for tower in towers if isinstance(tower, HouseTower))
        self.max_soldiers = max(1, house_count)

        if len(soldiers) < self.max_soldiers:
            self.spawn_soldier(soldiers, enemies)

        for soldier in soldiers:
            soldier.update(enemies)

    def spawn_soldier(self, soldiers, enemies):
        angle = 2 * math.pi * len(soldiers) / self.max_soldiers
        offset_x = self.spawn_radius * math.cos(angle)
        offset_y = self.spawn_radius * math.sin(angle)
        new_soldier = Soldier(self.world_x + offset_x, self.world_y + offset_y, soldiers, enemies, self.grid_x, self.grid_y)
        soldiers.append(new_soldier)
        print(f"Spawned soldier at {self.world_x + offset_x}, {self.world_y + offset_y}")
        
    def draw(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
        tower_sprite = self.sprite
        if camera.zoom < 1:
            scaled_width = int(tower_sprite.get_width() * camera.zoom)
            scaled_height = int(tower_sprite.get_height() * camera.zoom)
            scaled_sprite = pygame.transform.scale(tower_sprite, (scaled_width, scaled_height))
            screen.blit(scaled_sprite, (screen_x - scaled_sprite.get_width() // 2, screen_y - scaled_sprite.get_height() // 2 - 10))
        else:
            screen.blit(tower_sprite, (screen_x - tower_sprite.get_width() // 2, screen_y - tower_sprite.get_height() // 2))
        if self.health < self.max_health:
            self.draw_health_bar(screen, screen_x, screen_y, self.sprite)

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

    def draw_edit_mode_buttons(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
        if self.show_edit_buttons:
            button_width, button_height = 50, 25
            padding = 5
            upgrade_cost = self.get_upgrade_cost()
            
            self.delete_button_rect = pygame.Rect(screen_x - button_width - padding, screen_y, button_width, button_height)
            self.upgrade_button_rect = pygame.Rect(screen_x + padding, screen_y, button_width, button_height)

            pygame.draw.rect(screen, (255, 0, 0), self.delete_button_rect)
            pygame.draw.rect(screen, (0, 255, 0), self.upgrade_button_rect)

            font = pygame.font.Font(None, 20)
            delete_text = font.render('Del', True, (255, 255, 255))
            upgrade_text = font.render('Upg', True, (255, 255, 255))
            screen.blit(delete_text, (self.delete_button_rect.x + 5, self.delete_button_rect.y + 5))
            screen.blit(upgrade_text, (self.upgrade_button_rect.x + 5, self.upgrade_button_rect.y + 5))
            
            cost_text = font.render(f"${upgrade_cost}", True, (255, 255, 255))
            screen.blit(cost_text, (self.upgrade_button_rect.x, self.upgrade_button_rect.bottom + 3))

    def upgrade(self):
        if self.level < len(self.upgrade_costs):
            self.level += 1
            self.max_soldiers += 1 
            self.health += 200
            self.max_health = self.health
            self.sprite = self.load_sprite()
            print(f"Barrack Tower upgraded to level {self.level}. Max soldiers: {self.max_soldiers}")
        else:
            print("Maximum level reached.")
