class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class GameContext(metaclass=SingletonMeta):
    def __init__(self, screen, tile_map, currency_handler, state_handler, phase_handler, main_tower):
        self.screen = screen
        self.tile_map = tile_map
        self._towers = []
        self._enemies = []
        self._soldiers = []
        self.currency_handler = currency_handler
        self.state_handler = state_handler
        self._camera = None
        self._tower_placement_handler = None
        self.phase_handler = phase_handler
        self.main_tower = main_tower

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, value):
        self._screen = value

    @property
    def tile_map(self):
        return self._tile_map

    @tile_map.setter
    def tile_map(self, value):
        self._tile_map = value

    @property
    def towers(self):
        return self._towers

    def add_tower(self, tower):
        self._towers.append(tower)

    def remove_tower(self, tower):
        self._towers.remove(tower)

    @property
    def enemies(self):
        return self._enemies

    @enemies.setter
    def enemies(self, value):
        self._enemies = value

    @property
    def soldiers(self):
        return self._soldiers

    def add_soldier(self, soldier):
        self._soldiers.append(soldier)

    def remove_soldier(self, soldier):
        self._soldiers.remove(soldier)

    @property
    def currency_handler(self):
        return self._currency_handler

    @currency_handler.setter
    def currency_handler(self, value):
        self._currency_handler = value

    @property
    def state_handler(self):
        return self._state_handler

    @state_handler.setter
    def state_handler(self, value):
        self._state_handler = value

    @property
    def camera(self):
        return self._camera

    @camera.setter
    def camera(self, value):
        self._camera = value

    @property
    def zoom(self):
        return self._camera.zoom if self._camera else 1.0

    @property
    def tower_placement_handler(self):
        return self._tower_placement_handler

    @tower_placement_handler.setter
    def tower_placement_handler(self, value):
        self._tower_placement_handler = value

    @property
    def main_tower(self):
        return self._main_tower

    @main_tower.setter
    def main_tower(self, value):
        self._main_tower = value

    def refresh_enemies(self):
        self.enemies = self.phase_handler.get_enemies()