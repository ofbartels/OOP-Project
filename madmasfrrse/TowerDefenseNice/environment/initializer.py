from .tilemap import TileMap
from .tile import Tile

class TileMapInitializer:
    def __init__(self, rows: int, cols: int, tile_type: str = 'grass'):
        self.rows = rows
        self.cols = cols
        self.tile_type = tile_type

    def initialize_tilemap(self) -> TileMap:
        tilemap = TileMap(self.rows, self.cols)

        for y in range(self.rows):
            for x in range(self.cols):
                tilemap.tiles[y][x] = Tile(x, y, self.tile_type)

        tilemap.populate_with_objects()

        return tilemap