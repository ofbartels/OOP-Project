import unittest
from madmasfrrse.entities.projectile import Projectile

class TestProjectile(unittest.TestCase):
    def setUp(self):
        """Setup for test cases."""
        self.projectile = Projectile(world_x=50, world_y=50, target_x=100, target_y=100, damage=50, speed=10)

    def test_initial_position(self):
        """Test the initial position of the projectile."""
        self.assertEqual(self.projectile.world_x, 50)
        self.assertEqual(self.projectile.world_y, 50)

    def test_initial_damage(self):
        """Test the initial damage set for the projectile."""
        self.assertEqual(self.projectile.damage, 50)

    def test_movement_towards_target(self):
        """Test projectile movement towards a target."""
        initial_distance = self.projectile.calculate_distance(self.projectile.target_x, self.projectile.target_y)
        self.projectile.move()
        new_distance = self.projectile.calculate_distance(self.projectile.target_x, self.projectile.target_y)
        self.assertTrue(new_distance < initial_distance)

    def test_impact(self):
        """Test impact functionality of the projectile."""
        # Assuming there is a method to handle impact logic which sets active to False when hitting a target
        self.projectile.impact()
        self.assertFalse(self.projectile.active)

if __name__ == '__main__':
    unittest.main()