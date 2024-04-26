import unittest
from madmasfrrse.entities.base_entity import BaseEntity, MovingEntity

class TestBaseEntity(unittest.TestCase):
    def test_base_entity_initialization(self):
        """Test that base entities are initialized with correct position."""
        entity = BaseEntity(world_x=100, world_y=200)
        self.assertEqual(entity.world_x, 100)
        self.assertEqual(entity.world_y, 200)

class TestMovingEntity(unittest.TestCase):
    def test_moving_entity_initialization(self):
        """Test that moving entities are initialized with correct attributes."""
        moving_entity = MovingEntity(world_x=150, world_y=250, health=500, radius=20)
        self.assertEqual(moving_entity.world_x, 150)
        self.assertEqual(moving_entity.world_y, 250)
        self.assertEqual(moving_entity.health, 500)
        self.assertEqual(moving_entity.radius, 20)

    def test_health_reduction(self):
        """Test that health reduction behaves correctly."""
        moving_entity = MovingEntity(world_x=150, world_y=250, health=500, radius=20)
        moving_entity.reduce_health(100)
        self.assertEqual(moving_entity.health, 400)
        moving_entity.reduce_health(500)
        self.assertEqual(moving_entity.health, 0)  # Ensure health does not go negative

    def test_draw_health(self):
        """Placeholder test for draw_health method."""
        moving_entity = MovingEntity(world_x=150, world_y=250, health=500, radius=20)
        # This would normally require a mock object for the screen
        # self.assertIsNone(moving_entity.draw_health(None))

if __name__ == '__main__':
    unittest.main()