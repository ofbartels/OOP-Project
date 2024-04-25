import random
from entities.enemy import Enemy
from settings import settings

class PhaseHandler:
    def __init__(self):
        self.waves = [
            {'enemies': 5, 'type': 'goblin', 'interval': 2000},
            {'enemies': 10, 'type': 'goblin_bomber', 'interval': 1000},
            {'enemies': 15, 'type': 'mixed', 'interval': 500}
        ]
        self.current_wave_index = 0
        self.enemies = []
        self.phase_active = False
        self.last_spawn_time = 0
        self.spawn_interval = 1000

    def update(self, current_time):
        if self.phase_active and current_time - self.last_spawn_time >= self.spawn_interval:
            if self.enemies_to_spawn > 0:
                self.spawn_enemy(self.current_type)
                self.enemies_to_spawn -= 1
                self.last_spawn_time = current_time

        if not self.enemies and self.phase_active:
            self.phase_active = False
            print("All enemies defeated. Returning to build mode.")
            return True

        return False

    def start_next_wave(self):
        if self.current_wave_index < len(self.waves):
            wave = self.waves[self.current_wave_index]
            self.enemies_to_spawn = wave['enemies']
            self.current_type = wave['type']
            self.spawn_interval = wave.get('interval', 1000)
            self.last_spawn_time = 0
            self.phase_active = True
            self.current_wave_index += 1

    def spawn_enemy(self, type):
        side = random.choice(['left', 'right', 'top', 'bottom'])
        grid_x = random.randint(0, settings.COLS - 1) if side in ['top', 'bottom'] else (0 if side == 'left' else settings.COLS - 1)
        grid_y = random.randint(0, settings.ROWS - 1) if side in ['left', 'right'] else (0 if side == 'top' else settings.ROWS - 1)
        
        if type == 'mixed':
            type = random.choice(['minotaur', 'goblin', 'goblin_bomber', 'eyeball'])
        
        new_enemy = Enemy(grid_x, grid_y, enemy_type=type)
        self.enemies.append(new_enemy)

    def get_enemies(self):
        self.enemies = [enemy for enemy in self.enemies if not enemy.is_destroyed]
        return self.enemies
