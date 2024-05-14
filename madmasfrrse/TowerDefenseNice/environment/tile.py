import pygame
from typing import Dict
from settings import settings

class Tile:
    tile_images: Dict[str, pygame.Surface] = {}

    def __init__(self, grid_x: int, grid_y: int, tile_type: str = 'grass'):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.world_x, self.world_y = settings.iso_projection(grid_x, grid_y)
        self.z_index = self.grid_y + self.grid_x
        self.tile_type = tile_type
        self.occupied = False

        if tile_type not in self.tile_images:
            self.tile_images[tile_type] = self._load_image(self._get_image_path(tile_type))

        self.image = self.tile_images[tile_type]
        self.image_cache = {}

    @staticmethod
    def _get_image_path(tile_type: str) -> str:
        image_paths = {
            'grass': 'assets/sprites/environment/tiles/grass.png',
            'river_straight': 'supply/Environment/river_straight.png',
            'river_corner': 'supply/Environment/river_corner.png',
        }
        return image_paths.get(tile_type, '')

    @staticmethod
    def _load_image(image_path: str) -> pygame.Surface:
        try:
            return pygame.image.load(image_path).convert_alpha()
        except pygame.error as e:
            print(f"Failed to load image at path: {image_path}. Error: {e}")
            return None

    def draw(self, screen: pygame.Surface, camera, zoom):
        if not self.image:
            return None

        zoom_key = round(zoom, 2)

        if zoom_key not in self.image_cache:
            self.image_cache[zoom_key] = pygame.transform.smoothscale(
                self.image, (int(self.image.get_width() * zoom), int(self.image.get_height() * zoom))
            )

        scaled_image = self.image_cache[zoom_key]
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
        rect = scaled_image.get_rect(center=(screen_x, screen_y))
        screen.blit(scaled_image, rect)
        return rect

    @classmethod
    def create_tile(cls, grid_x: int, grid_y: int, tile_type: str = 'grass') -> 'Tile':
        return cls(grid_x, grid_y, tile_type)