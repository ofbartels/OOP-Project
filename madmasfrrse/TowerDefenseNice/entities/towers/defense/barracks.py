from entities.soldier import Soldier
from entities.towers.defense_towers import DefenseTower
import random, math

class BarracksTower(DefenseTower):
    upgrade_costs = [800, 1200, 2000]
    max_soldiers_per_level = [2, 5, 8]

    def __init__(self, grid_x, grid_y, building_type='barracks', level=1):
        super().__init__(grid_x, grid_y, building_type, level)
        self.spawn_radius = 10
        self.max_soldiers = self.max_soldiers_per_level[level - 1]
        self.health = self.max_health = 1000

    def load_sprite(self):
        return super().load_sprite()

    def update(self, current_time, game_context):
        self.combat_update(game_context)

    def combat_update(self, game_context):
        from ..economy.house import HouseTower  # Import HouseTower locally to avoid circular import
        house_count = sum(isinstance(tower, HouseTower) for tower in game_context.towers)
        self.max_soldiers = min(self.max_soldiers_per_level[self.level - 1], max(1, house_count))
        if len(game_context.soldiers) < self.max_soldiers:
            self.spawn_soldier(game_context.soldiers, game_context.enemies)
        for soldier in game_context.soldiers:
            soldier.update()
            soldier.draw(game_context.screen, game_context.camera)

    def spawn_soldier(self, soldiers, enemies):
        if len(soldiers) < self.max_soldiers:
            angle = random.uniform(0, 2 * math.pi)
            spawn_radius = 50
            offset_x = spawn_radius * math.cos(angle) - 20
            offset_y = spawn_radius * math.sin(angle) + 50
            new_soldier = Soldier(self.world_x + offset_x, self.world_y + offset_y, soldiers, enemies)
            soldiers.append(new_soldier)
            print(f"Spawned soldier at {self.world_x + offset_x}, {self.world_y + offset_y}")

    def upgrade(self):
        if self.level < len(self.upgrade_costs):
            self.level += 1
            self.max_soldiers = self.max_soldiers_per_level[self.level - 1]
            self.health += 100
            self.max_health = self.health
            self.sprite = self.load_sprite()
            print(f"Barracks Tower upgraded to level {self.level}. Max soldiers: {self.max_soldiers}")
        else:
            print("Maximum level reached.")