from ..enemy import Enemy
import pygame

class Goblin(Enemy):
    def __init__(self, grid_x, grid_y):
        super().__init__(grid_x, grid_y, enemy_type='goblin', radius=30, health=1500)
        self.speed = 120
        self.combat_row = 4

    def update(self, towers, delta_time, main_tower, enemies):
        super().update(towers, delta_time, main_tower, enemies)

    def draw_health_bar(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
        bar_length = 50
        bar_height = 5
        fill = (self.health / self.max_health) * bar_length
        pygame.draw.rect(screen, (255, 0, 0), (screen_x - bar_length // 2, screen_y - 20, bar_length, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (screen_x - bar_length // 2, screen_y - 20, fill, bar_height))

    def draw(self, screen, camera):
        super().draw(screen, camera)
        self.draw_health_bar(screen, camera)
