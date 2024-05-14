import random
from typing import List, Tuple
from environment.tile import Tile
from environment.objects.factories import StoneFactory, TreeFactory
from environment.objects.game_object import GameObject
from settings import settings

class TileMap:
    def __init__(self, rows: int, cols: int, center_area_size: Tuple[int, int] = (3, 3)):
        self._rows = rows
        self._cols = cols
        self.tiles = [[Tile(x, y) for x in range(cols)] for y in range(rows)]
        self.objects: List[GameObject] = []
        self._center_area_size = center_area_size
        self._center_x = cols // 2 - 2
        self._center_y = rows // 2 - 2
        
        self.stone_factory = StoneFactory()
        self.tree_factory = TreeFactory()

    @property
    def center_x(self) -> int:
        return self._center_x

    @center_x.setter
    def center_x(self, value: int):
        self._center_x = max(0, min(value, self.cols - 1))

    @property
    def center_y(self) -> int:
        return self._center_y

    @center_y.setter
    def center_y(self, value: int):
        self._center_y = max(0, min(value, self.rows - 1))

    @property
    def rows(self) -> int:
        return self._rows

    @rows.setter
    def rows(self, value: int):
        self._rows = max(0, value)

    @property
    def cols(self) -> int:
        return self._cols

    @cols.setter
    def cols(self, value: int):
        self._cols = max(0, value)

    @property
    def center_area_size(self) -> Tuple[int, int]:
        return self._center_area_size

    @center_area_size.setter
    def center_area_size(self, value: Tuple[int, int]):
        self._center_area_size = (max(1, value[0]), max(1, value[1]))

    def populate_with_objects(self):
        for row in self.tiles:
            for tile in row:
                if random.random() < 0.3:
                    factory = self.tree_factory if random.random() < 0.6 else self.stone_factory
                    obj = factory.create_object(tile)
                    self.objects.append(obj)

    def draw(self, game_context):
        updated_rects = []

        for row in self.tiles:
            for tile in row:
                rect = tile.draw(game_context.screen, game_context.camera, game_context.zoom)
                if rect:
                    updated_rects.append(rect)

        for obj in self.objects:
            rect = obj.draw(game_context)
            if rect:
                updated_rects.append(rect)

        return updated_rects

    def get_clicked_tile(self, screen_x: int, screen_y: int, game_context) -> Tile:
        world_x, world_y = game_context.camera.screen_to_world(screen_x, screen_y)
        grid_x, grid_y = settings.inverse_iso_projection(world_x, world_y)

        if 0 <= grid_x < self.cols and 0 <= grid_y < self.rows:
            return self.tiles[grid_y][grid_x]

        return None

    def can_place_tower(self, tile) -> bool:
        return tile and not tile.occupied

    def place_tower(self, tile, tower, game_context) -> bool:
        if self.can_place_tower(tile):
            tile.occupied = True
            game_context.towers.append(tower)
            return True
        return False

    def get_center_tiles(self) -> List[Tuple[int, int]]:
        return [(x, y) for y in range(self.center_y - self.center_area_size[1] // 2, self.center_y + self.center_area_size[1] // 2 + 1)
                for x in range(self.center_x - self.center_area_size[0] // 2, self.center_x + self.center_area_size[0] // 2 + 1)]