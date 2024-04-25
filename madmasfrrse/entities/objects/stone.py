import pygame
import random

class Stone:
    def __init__(self):
        stone_sprites = [
            ('supply/Enviroument/Spring/stones/stone(1).png', (0, 25)),
            ('supply/Enviroument/Spring/stones/stone(3).png', (0, 25)),
            ('supply/Enviroument/Spring/stones/stone(2).png', (0, 25)),
            ('supply/Enviroument/Spring/stones/stone(1).png', (0, 25)),
        ]
        sprite_path, self.base_offsets = random.choice(stone_sprites)
        self.sprite = pygame.image.load(sprite_path).convert_alpha()
        self.occupied = True
        self.type = 'stone'

    def place_on_tile(self, tile):
        self.world_x, self.world_y = tile.world_x, tile.world_y
        self.z_index = tile.z_index

    def draw(self, screen, camera):
        offset_x, offset_y = self.base_offsets[0], self.base_offsets[1]
        if camera.zoom < 1:
            offset_y -= 10

        screen_x, screen_y = camera.world_to_screen(self.world_x + offset_x, self.world_y + offset_y)
        screen.blit(self.sprite, (screen_x - self.sprite.get_width() // 2, screen_y - self.sprite.get_height() // 2))
