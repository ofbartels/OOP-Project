import pygame
from events.state_handler import GameStates
from entities.towers.economy_tower import EconomyTower

class WheatTower(EconomyTower):
    def __init__(self, grid_x, grid_y, building_type='wheat', level=1):
        super().__init__(grid_x, grid_y, building_type, level)
        self.level_up_rate = 1000
        self.last_level_up_time = pygame.time.get_ticks()
        self.max_level = 4
        self.active_cycle = True
        self.health = self.max_health = 100

    def load_sprite(self):
        return super().load_sprite()

    def update(self, current_time, game_context):
        if game_context.state_handler.current_state != GameStates.GAME_PLAY:
            return

        if current_time - self._last_level_up_time > self._level_up_rate:
            self.level = (self.level % self._max_level) + 1
            if self.level == 1:
                game_context.currency_handler.add_currency(self._currency_add_amount)
                print(f"{self.building_type} Tower at ({self.grid_x}, {self.grid_y}) reset to level 1 and added {self._currency_add_amount} currency.")
            else:
                print(f"{self.building_type} Tower at ({self.grid_x}, {self.grid_y}) leveled up to {self.level}.")
            self._last_level_up_time = current_time
            self._sprite = self.load_sprite()

    def reduce_level_up_time(self, reduction_factor=0.8):
        self._level_up_rate = int(self._level_up_rate * reduction_factor)
        print(f"{self.building_type} Tower at ({self.grid_x}, {self.grid_y}) level up time reduced to {self._level_up_rate} ms.")