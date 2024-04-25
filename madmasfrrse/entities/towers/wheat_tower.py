import pygame
from ..base_tower import Tower

class WheatTower(Tower):
    def __init__(self, grid_x, grid_y, building_type='wheat', level=1):
        super().__init__(grid_x, grid_y, building_type, level)
        self.level_up_rate = 1000
        self.level_up_rate_always = 1000
        self.last_level_up_time = pygame.time.get_ticks()
        self.max_level = 4
        self.active_cycle = True
        self.world_y += 10
        self.health = self.max_health = 100

    def special_update(self, current_time, currency_handler):
        if not self.active_cycle:
            return

        if current_time - self.last_level_up_time > self.level_up_rate:
            self.level = (self.level % self.max_level) + 1
            if self.level == 1:
                currency_handler.add_currency(500)
                print(f"{self.building_type} Tower at ({self.grid_x}, {self.grid_y}) reset to level 1 and added 500 currency.")
            else:
                print(f"{self.building_type} Tower at ({self.grid_x}, {self.grid_y}) leveled up to {self.level}.")
            self.last_level_up_time = current_time
            self.sprite = self.load_sprite()

    def end_of_phase(self):
        self.active_cycle = False

    def draw(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
        tower_sprite = self.sprite
        if camera.zoom < 1:
            scaled_width = int(tower_sprite.get_width() * camera.zoom)
            scaled_height = int(tower_sprite.get_height() * camera.zoom)
            scaled_sprite = pygame.transform.scale(tower_sprite, (scaled_width, scaled_height))
            screen.blit(scaled_sprite, (screen_x - scaled_sprite.get_width() // 2, screen_y - scaled_sprite.get_height() // 2 - 6))
        else:
            screen.blit(tower_sprite, (screen_x - tower_sprite.get_width() // 2, screen_y - tower_sprite.get_height() // 2 + 3))

        if self.health < self.max_health:
            self.draw_health_bar(screen, screen_x, screen_y, tower_sprite)

    def draw_health_bar(self, screen, screen_x, screen_y, sprite):
        bar_length = 40
        bar_height = 5
        health_ratio = self.health / self.max_health
        fill_length = int(bar_length * health_ratio)
        bar_x = screen_x - bar_length // 2
        bar_y = screen_y - sprite.get_height() // 2 - 10
        pygame.draw.rect(screen, (128, 128, 128), (bar_x, bar_y, bar_length, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_length, bar_height))

    def reduce_level_up_time(self):
        self.level_up_rate = 100
        
    def draw_edit_mode_buttons(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
        if self.show_edit_buttons:
            button_width, button_height = 50, 25
            padding = 5
            
            self.delete_button_rect = pygame.Rect(screen_x - button_width - padding, screen_y, button_width, button_height)

            pygame.draw.rect(screen, (255, 0, 0), self.delete_button_rect)

            font = pygame.font.Font(None, 20)
            delete_text = font.render('Del', True, (255, 255, 255))
            screen.blit(delete_text, (self.delete_button_rect.x + 5, self.delete_button_rect.y + 5))
            
    def upgrade(self):
        pass