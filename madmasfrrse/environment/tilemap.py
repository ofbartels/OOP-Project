from .tile import Tile
from settings import settings

from .tile import Tile
from entities.objects.tree import Tree
from entities.objects.stone import Stone
from settings import settings
import random

from environment.decorations.cloud import CloudDecoration

class TileMap:
    def __init__(self, rows, cols, default_image_path, special_image_path, center_area_size=(3, 3)):
        self.rows = rows
        self.cols = cols
        self.center_area_size = center_area_size
        self.center_x = cols // 2 - 2
        self.center_y = rows // 2 - 2
        self.clouds = [CloudDecoration(random.randint(0, 800), random.randint(0, 600)) for _ in range(5)]  # Assuming screen width of 800px      
        self.tiles = []
        for y in range(rows):
            row = []
            for x in range(cols):
                if self._is_in_center_area(x, y, self.center_x, self.center_y):
                    tile = Tile(x, y, (0, 0, 0), special_image_path)
                else:
                    tile = Tile(x, y, (0, 0, 0), default_image_path)
                    if random.random() < 0.15:  # 15% chance of something being placed
                        if random.random() < 0.75:  # 75% of that 15% for a tree (i.e., ~11.25% total)
                            tile.set_object(Tree(), 'tree')
                        else:  # 25% of that 15% for a stone (i.e., ~3.75% total)
                            tile.set_object(Stone(), 'stone')
                row.append(tile)
            self.tiles.append(row)

    def get_center_tiles(self):
        # Return the coordinates of the center tiles
        return [(x, y) for y in range(self.center_y - self.center_area_size[1]//2, self.center_y + self.center_area_size[1]//2 + 1)
                for x in range(self.center_x - self.center_area_size[0]//2, self.center_x + self.center_area_size[0]//2 + 1)]
    
    def _is_in_center_area(self, x, y, center_x, center_y):
        x_in_range = center_x - self.center_area_size[0]//2  <= x < center_x + self.center_area_size[0]//2 + 3
        y_in_range = center_y - self.center_area_size[1]//2  <= y < center_y + self.center_area_size[1]//2 +3 
        return x_in_range and y_in_range

    def draw(self, screen, camera):
        updated_areas = []
        for row in self.tiles:
            for tile in row:
                rect = tile.draw(screen, camera)
                updated_areas.append(rect)
        return updated_areas

    def get_clicked_tile(self, mouse_x, mouse_y, camera):
        world_x, world_y = camera.screen_to_world(mouse_x, mouse_y)
        grid_x, grid_y = settings.inverse_iso_projection(world_x, world_y)
        if 0 <= grid_x < self.cols and 0 <= grid_y < self.rows:
            return self.tiles[grid_y][grid_x]
        return None
