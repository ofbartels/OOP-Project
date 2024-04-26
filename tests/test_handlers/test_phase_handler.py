import unittest
from unittest.mock import patch
from madmasfrrse.handlers.phase_handler import PhaseHandler

class TestPhaseHandler(unittest.TestCase):
    def setUp(self):
        """Setup for PhaseHandler tests."""
        self.phase_handler = PhaseHandler()

    def test_initial_state(self):
        """Test the initial state of PhaseHandler."""
        self.assertEqual(len(self.phase_handler.waves), 3)
        self.assertFalse(self.phase_handler.phase_active)
        self.assertEqual(self.phase_handler.current_wave_index, 0)

    def test_start_next_wave(self):
        """Test starting the next wave."""
        self.phase_handler.start_next_wave()
        self.assertTrue(self.phase_handler.phase_active)
        self.assertEqual(self.phase_handler.current_wave_index, 1)
        self.assertEqual(self.phase_handler.enemies_to_spawn, 5)  # First wave settings

    @patch('madmasfrrse.handlers.phase_handler.PhaseHandler.spawn_enemy')
    def test_wave_update(self, mock_spawn):
        """Test updating within a wave."""
        self.phase_handler.start_next_wave()
        self.phase_handler.update(1001)
        mock_spawn.assert_called_once()
        self.assertEqual(self.phase_handler.last_spawn_time, 1001)

    def test_all_enemies_defeated(self):
        """Test handling all enemies defeated."""
        self.phase_handler.start_next_wave()
        self.phase_handler.update(2000)  # Simulate time for spawns to complete
        self.phase_handler.enemies.clear()  # Simulate all enemies defeated
        result = self.phase_handler.update(3000)  # Additional update call
        self.assertFalse(self.phase_handler.phase_active)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()