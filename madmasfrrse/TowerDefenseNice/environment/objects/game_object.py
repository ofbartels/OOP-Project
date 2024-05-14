from abc import ABC, abstractmethod

class GameObject(ABC):
    def __init__(self, tile):
        self._world_x, self._world_y = tile.world_x, tile.world_y
        self._z_index = tile.z_index
        self._sprite = None

    @abstractmethod
    def _load_sprite(self):
        pass

    def draw(self, game_context):
        if self._sprite is None:
            self._sprite = self._load_sprite()
        game_context.screen.blit(self._sprite, (self._world_x, self._world_y))

    @property
    def world_x(self):
        return self._world_x

    @property
    def world_y(self):
        return self._world_y

    @property
    def z_index(self):
        return self._z_index