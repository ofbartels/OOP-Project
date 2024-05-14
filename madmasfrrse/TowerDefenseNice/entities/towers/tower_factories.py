from abc import ABC, abstractmethod
from .economy import WheatTower, CornTower, HouseTower, MillTower, BlacksmithTower
from .defense import ArcherTower, BallistaTower, BarracksTower, WizardTower

class TowerFactory(ABC):
    @abstractmethod
    def create_tower(self, grid_x, grid_y, building_type, level):
        pass

class EconomyTowerFactory(TowerFactory):
    def create_tower(self, grid_x, grid_y, building_type, level):
        if building_type == 'wheat':
            return WheatTower(grid_x, grid_y, building_type, level)
        elif building_type == 'corn':
            return CornTower(grid_x, grid_y, building_type, level)
        elif building_type == 'house':
            return HouseTower(grid_x, grid_y, building_type, level)
        elif building_type == 'mill':
            return MillTower(grid_x, grid_y, building_type, level)
        elif building_type == 'smith':
            return BlacksmithTower(grid_x, grid_y, building_type, level)
        else:
            raise ValueError(f"Invalid economy tower type: {building_type}")

class DefenseTowerFactory(TowerFactory):
    def create_tower(self, grid_x, grid_y, building_type, level):
        if building_type == 'archer':
            return ArcherTower(grid_x, grid_y, building_type, level)
        elif building_type == 'ballista':
            return BallistaTower(grid_x, grid_y, building_type, level)
        elif building_type == 'barracks':
            return BarracksTower(grid_x, grid_y, building_type, level)
        elif building_type == 'wizard':
            return WizardTower(grid_x, grid_y, building_type, level)
        else:
            raise ValueError(f"Invalid defense tower type: {building_type}")