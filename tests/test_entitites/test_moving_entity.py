import unittest
from madmasfrrse.entities.base_entity import MovingEntity

class TestMovingEntity(unittest.TestCase):
    def setUp(self):
        """Setup for test cases."""
        self.moving_entity = MovingEntity(world_x=100, world_y=100, health=500, radius=20)

    def test_initial_position(self):
        """Test the initial position of the moving entity."""
        self.assertEqual(self.moving_entity.world_x, 100)
        self.assertEqual(self.moving_entity.world_y, 100)

    def test_health_initialization(self):
        """Test the initial health of the moving entity."""
        self.assertEqual(self.moving_entity.health, 500)

    def test_move(self):
        """Test movement functionality."""
        # Example movement functionality, assuming there is a method to update position
        self.moving_entity.move(10, 15)  # Assuming move method adjusts x, y by given offsets
        self.assertEqual(self.moving_entity.world_x, 110)
        self.assertEqual(self.moving_entity.world_y, 115)

    def test_health_reduction(self):
        """Test the health reduction mechanism."""
        self.moving_entity.reduce_health(100)
        self.assertEqual(self.moving_entity.health, 400)
        # Check boundary condition
        self.moving_entity.reduce_health(500)
        self.assertEqual(self.moving_entity.health, 0)  # Ensure health does not go negative

    def test_collision_detection(self):
        """Test collision detection logic."""
        # This will require a mock setup or additional detail about how collision detection is implemented
        # Example test for collision detection
        other_entity = MovingEntity(world_x=110, world_y=115, health=100, radius=10)
        self.assertTrue(self.moving_entity.detect_collision(other_entity))

if __name__ == '__main__':
    unittest.main()