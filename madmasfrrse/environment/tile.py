import pygame
from settings import settings
from entities import BaseEntity

class Tile(BaseEntity):
    def __init__(self, grid_x, grid_y, color, image_path=None):
        super().__init__(*settings.iso_projection(grid_x, grid_y))
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.color = color
        self.selected = False
        self.occupied = False
        self.z_index = grid_y + grid_x  
        self.rect = pygame.Rect(self.world_x, self.world_y, settings.TILE_WIDTH, settings.TILE_HEIGHT)
        self.image = self._load_image(image_path)
        self.object = None
        self.grass_image = None
    
    def _load_image(self, image_path):
        if image_path:
            return pygame.image.load(image_path).convert_alpha()
        return None

    def set_object(self, obj, obj_type):
        self.object = obj
        self.type = obj_type
        self.occupied = True
        obj.place_on_tile(self)  

    def draw(self, screen, camera):
        translated_x, translated_y = camera.world_to_screen(self.world_x, self.world_y)
        if self.image:
            screen.blit(self.image, (translated_x - self.image.get_width() // 2, translated_y - self.image.get_height() // 2))
        if self.grass_image:
            screen.blit(self.grass_image, (translated_x - self.grass_image.get_width() // 2, translated_y - self.grass_image.get_height() // 2))

    def _draw_polygon(self, screen, x, y):
        half_width = settings.TILE_WIDTH // 2
        half_height = settings.TILE_HEIGHT // 2
        points = [
            (x, y - half_height),
            (x + half_width, y),
            (x, y + half_height),
            (x - half_width, y),
        ]
        tile_color = settings.RED if self.occupied else (self.color if not self.selected else settings.YELLOW)
        pygame.draw.polygon(screen, tile_color, points)
        pygame.draw.lines(screen, settings.BLACK, True, points, 1)
