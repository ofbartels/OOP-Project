import pygame
from settings import settings

class MainTowerPart:
    def __init__(self, x, y, sprite, z_index):
        self.world_x, self.world_y = settings.iso_projection(x, y)
        self.sprite = sprite
        self.z_index = z_index
        self.is_destroyed = False

    def draw(self, screen, camera):
        if not self.is_destroyed:
            screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
            if camera.zoom < 1:
                screen.blit(self.sprite, (screen_x - self.sprite.get_width() // 2, screen_y - self.sprite.get_height() // 2 - 15))
            else:
                screen.blit(self.sprite, (screen_x - self.sprite.get_width() // 2, screen_y - self.sprite.get_height() // 2 + 5))

class MainTower:
    def __init__(self, tile_map, state_handler):
        self.state_handler = state_handler
        self.is_destroyed = False
        self.health = 3000
        self.max_health = 3000

        sprites = {
            (0, 0): 'supply/Castle/castle_wall(7).png',
            (0, 1): 'supply/Castle/castle_wall(4).png',
            (0, 2): 'supply/Castle/castle_wall(9).png',
            (1, 0): 'supply/Castle/castle_wall(1).png',
            (1, 1): 'supply/Towers/Red/castle_tower_red(5).png',
            (1, 2): 'supply/Castle/castle_wall(6).png',
            (2, 0): 'supply/Castle/castle_wall(8).png',
            (2, 1): 'supply/Castle/castle_wall(5).png',
            (2, 2): 'supply/Castle/castle_wall(10).png'
        }
        center_tiles = tile_map.get_center_tiles()
        self.parts = []
        sum_x = sum_y = 0
        for (x, y) in center_tiles:
            idx = (y - tile_map.center_y + 1, x - tile_map.center_x + 1)
            sprite = pygame.image.load(sprites[idx]).convert_alpha()
            z_index = y + x
            part = MainTowerPart(x, y, sprite, z_index)
            self.parts.append(part)
            sum_x += x
            sum_y += y

        self.world_x, self.world_y = settings.iso_projection(sum_x // len(center_tiles), sum_y // len(center_tiles))

    def draw(self, screen, camera):
        for part in self.parts:
            part.draw(screen, camera)
        if self.health < self.max_health:
            self.draw_health_bar(screen, camera)

    def draw_health_bar(self, screen, camera):
        middle_screen_x, middle_screen_y = camera.world_to_screen(self.world_x, self.world_y)
        bar_width = 100
        bar_height = 10
        health_ratio = self.health / self.max_health
        fill_width = int(bar_width * health_ratio)
        bar_x = middle_screen_x - bar_width // 2
        bar_y = middle_screen_y - 30 
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height))

    def update(self):
        if self.health <= 0:
            self.handle_destruction()

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.is_destroyed = True
            print("Main Tower destroyed. Game Over.")

    def handle_destruction(self):
        self.is_destroyed = True
        print("Main Tower destroyed. Game Over.")

    def reset_health(self):
        self.health = self.max_health
