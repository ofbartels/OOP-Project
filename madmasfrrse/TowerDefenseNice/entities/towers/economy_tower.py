import pygame
from events.state_handler import GameStates
from .tower_base import Tower

class EconomyTower(Tower):
    def __init__(self, grid_x, grid_y, building_type, level, currency_add_amount=50, level_up_rate=1000):
        super().__init__(grid_x, grid_y, building_type, level)
        self._last_level_up_time = pygame.time.get_ticks()
        self._max_level = 4
        self._active_cycle = True
        self._level_up_rate = level_up_rate
        self._currency_add_amount = currency_add_amount

    def update(self, current_time, game_context):
        pass

    def end_of_phase(self):
        self.health = self.max_health

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.mark_for_removal = True