from abc import ABC, abstractmethod
from ..tile import Tile
from .stone import Stone
from .tree import Tree

class GameObjectFactory(ABC):
    @abstractmethod
    def create_object(self, tile: Tile):
        """Create a new game object at the given tile."""
        pass

class StoneFactory(GameObjectFactory):
    def create_object(self, tile):
        return Stone(tile)

class TreeFactory(GameObjectFactory):
    def create_object(self, tile):
        return Tree(tile)