from ..base_tower import Tower
import pygame, random
from entities.villager import Villager

class HouseTower(Tower):
    def __init__(self, grid_x, grid_y, building_type='house', level=1):
        self.flipped = False
        self.color_variants = [
            'supply/Economy/house/Blue/wood_blue_house',
            'supply/Economy/house/Green/wood_green_house',
            'supply/Economy/house/Red/wood_red_house',
            'supply/Economy/house/Wood/wood_house',
        ]
        self.building_type = building_type
        self.color_variant = random.choice(self.color_variants)
        super().__init__(grid_x, grid_y, building_type, level)
        self.health = self.max_health = 500
        self.population = 0

    def load_sprite(self):
        sprite_path = f"{self.color_variant}({self.level}).png"
        sprite = pygame.image.load(sprite_path).convert_alpha()
        if self.flipped:
            sprite = pygame.transform.flip(sprite, True, False)
        return sprite

    def draw(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)

        if self.flipped:
            tower_sprite = pygame.transform.flip(self.sprite, True, False)
        else:
            tower_sprite = self.sprite

        if camera.zoom < 1:
            scaled_width = int(tower_sprite.get_width() * camera.zoom)
            scaled_height = int(tower_sprite.get_height() * camera.zoom)
            scaled_sprite = pygame.transform.scale(tower_sprite, (scaled_width, scaled_height))
            screen.blit(scaled_sprite, (screen_x - scaled_sprite.get_width() // 2, screen_y - scaled_sprite.get_height() // 2 + 10))
        else:
            screen.blit(tower_sprite, (screen_x - tower_sprite.get_width() // 2, screen_y - tower_sprite.get_height() // 2 + 20))
        
        if self.health < self.max_health:
            self.draw_health_bar(screen, screen_x, screen_y, tower_sprite)  # Ensure to pass the potentially flipped sprite

    def check_villagers(self, villagers):
        if self.population == 0:
            self.spawn_person(villagers)
            self.population = 1

    def spawn_person(self, villagers):
        print("sdfsdf")
        spawn_x = self.world_x + random.randint(-10, 10)
        spawn_y = self.world_y + random.randint(-10, 10)
        new_person = Villager(spawn_x, spawn_y, 'supply/villager.png')
        villagers.append(new_person)

    def draw_health_bar(self, screen, screen_x, screen_y, sprite):
        bar_length = 40
        bar_height = 5
        health_ratio = self.health / self.max_health
        fill_length = int(bar_length * health_ratio)
        bar_x = screen_x - bar_length // 2
        bar_y = screen_y - sprite.get_height() // 2 - 10

        pygame.draw.rect(screen, (128, 128, 128), (bar_x, bar_y, bar_length, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_length, bar_height))

    def flip_sprite(self):
        self.flipped = not self.flipped
        self.sprite = self.load_sprite()
        
    def draw_edit_mode_buttons(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
        if self.show_edit_buttons:
            button_width, button_height = 40, 20
            padding = 10

            base_x = screen_x - (2 * button_width + 3 * padding) / 2 - 35
            base_y = screen_y - button_height - padding

            self.delete_button_rect = pygame.Rect(base_x, base_y, button_width, button_height)
            self.left_button_rect = pygame.Rect(base_x + 2 * (button_width + padding), base_y, button_width, button_height)
            self.right_button_rect = pygame.Rect(base_x + 3 * (button_width + padding), base_y, button_width, button_height)

            pygame.draw.rect(screen, (255, 255, 255), self.delete_button_rect)
            pygame.draw.rect(screen, (255, 255, 255), self.left_button_rect)
            pygame.draw.rect(screen, (255, 255, 255), self.right_button_rect)

            font = pygame.font.Font(None, 18)
            delete_text = font.render('Del', True, (0, 0, 0))
            left_text = font.render('<', True, (0, 0, 0))
            right_text = font.render('>', True, (0, 0, 0))
            
            screen.blit(delete_text, (self.delete_button_rect.x + 10, self.delete_button_rect.y + 3))
            screen.blit(left_text, (self.left_button_rect.x + 14, self.left_button_rect.y + 3))
            screen.blit(right_text, (self.right_button_rect.x + 14, self.right_button_rect.y + 3))
