import unittest
from unittest.mock import MagicMock
from madmasfrrse.entities.towers.archer_tower import ArcherTower
from madmasfrrse.entities.towers.wizard_tower import WizardTower
from madmasfrrse.entities.towers.house_tower import HouseTower
from madmasfrrse.entities.enemy import Enemy

class TestArcherTower(unittest.TestCase):
    def setUp(self):
        """Setup for Archer Tower tests."""
        self.archer_tower = ArcherTower(world_x=100, world_y=100)

    def test_initialization(self):
        """Test the initialization of Archer Tower."""
        self.assertEqual(self.archer_tower.world_x, 100)
        self.assertEqual(self.archer_tower.world_y, 100)
        self.assertIsNotNone(self.archer_tower.attack_range)
        self.assertIsNotNone(self.archer_tower.damage)

    def test_attack(self):
        """Test Archer Tower's attack functionality."""
        # Assuming there's an attack method which also handles target acquisition
        target = MagicMock(spec=Enemy)
        target.health = 100
        target.world_x = 110
        target.world_y = 110
        self.archer_tower.attack([target])
        self.assertLess(target.health, 100)

class TestWizardTower(unittest.TestCase):
    def setUp(self):
        """Setup for Wizard Tower tests."""
        self.wizard_tower = WizardTower(world_x=200, world_y=200)

    def test_initialization(self):
        """Test the initialization of Wizard Tower."""
        self.assertEqual(self.wizard_tower.world_x, 200)
        self.assertEqual(self.wizard_tower.world_y, 200)
        self.assertIsNotNone(self.wizard_tower.magic_power)

    def test_cast_spell(self):
        """Test Wizard Tower's spell casting functionality."""
        # Assuming a method that casts spells
        effectiveness = self.wizard_tower.cast_spell()
        self.assertTrue(effectiveness > 0)

class TestHouseTower(unittest.TestCase):
    def setUp(self):
        """Setup for House Tower tests."""
        self.house_tower = HouseTower(world_x=300, world_y=300)

    def test_initialization(self):
        """Test the initialization of House Tower."""
        self.assertEqual(self.house_tower.world_x, 300)
        self.assertEqual(self.house_tower.world_y, 300)
        self.assertIsNotNone(self.house_tower.residents)

    def test_produce(self):
        """Test House Tower's resource production functionality."""
        resources_before = self.house_tower.produce_resources()
        resources_after = self.house_tower.produce_resources()
        self.assertTrue(resources_after > resources_before)

if __name__ == '__main__':
    unittest.main()