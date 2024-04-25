from ..base_tower import Tower
import pygame, random

class BallistaTower(Tower):
    def __init__(self, grid_x, grid_y, building_type='ballista', level=1):
        super().__init__(grid_x, grid_y, building_type, level)
        self.building_type = building_type
        self.health = self.max_health = 1000
