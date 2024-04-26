import unittest
from madmasfrrse.entities.enemies.goblin import Goblin
from madmasfrrse.entities.enemies.minotaur import Minotaur
from madmasfrrse.entities.enemies.eyeball import Eyeball
from madmasfrrse.entities.enemy import Enemy

class TestGoblin(unittest.TestCase):
    def test_goblin_initialization(self):
        """Test Goblin initialization."""
        goblin = Goblin(grid_x=10, grid_y=20)
        self.assertEqual(goblin.grid_x, 10)
        self.assertEqual(goblin.grid_y, 20)
        self.assertEqual(goblin.enemy_type, 'goblin')
        self.assertEqual(goblin.health, 1500)  # Example health, replace with actual if different

    def test_goblin_update(self):
        """Test Goblin update mechanics. Placeholder for actual functionality."""
        goblin = Goblin(grid_x=10, grid_y=20)
        # Assume mock setup for the game environment here
        # Example: goblin.update(towers=[], delta_time=1, main_tower=None, enemies=[])
        # Check expected state change if any, example:
        # self.assertEqual(goblin.health, expected_health_after_update)

class TestMinotaur(unittest.TestCase):
    def test_minotaur_initialization(self):
        """Test Minotaur initialization with correct settings."""
        minotaur = Minotaur(grid_x=5, grid_y=15)
        self.assertEqual(minotaur.grid_x, 5)
        self.assertEqual(minotaur.grid_y, 15)
        self.assertEqual(minotaur.enemy_type, 'minotaur')
        self.assertEqual(minotaur.health, 150)  # Example health

class TestEyeball(unittest.TestCase):
    def test_eyeball_initialization(self):
        """Test Eyeball enemy initialization."""
        eyeball = Eyeball(grid_x=3, grid_y=8)
        self.assertEqual(eyeball.grid_x, 3)
        self.assertEqual(eyeball.grid_y, 8)
        self.assertEqual(eyeball.enemy_type, 'eyeball')
        self.assertEqual(eyeball.health, 150)  # Example health

if __name__ == '__main__':
    unittest.main()