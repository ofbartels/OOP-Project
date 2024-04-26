import unittest
from madmasfrrse.handlers.state_handler import StateHandler, GameStates

class TestStateHandler(unittest.TestCase):
    def setUp(self):
        """Setup for StateHandler tests."""
        self.state_handler = StateHandler()

    def test_initial_state(self):
        """Test the initial state of StateHandler."""
        self.assertEqual(self.state_handler.current_state, GameStates.START_MENU)

    def test_change_state(self):
        """Test state change functionality."""
        self.state_handler.change_state(GameStates.BUILD_MODE)
        self.assertEqual(self.state_handler.current_state, GameStates.BUILD_MODE)

    def test_start_game_from_menu(self):
        """Test starting the game from the start menu."""
        self.state_handler.start_game()
        self.assertEqual(self.state_handler.current_state, GameStates.BUILD_MODE)

    def test_start_game_from_other_state(self):
        """Test starting the game from a non-menu state does not change state."""
        self.state_handler.change_state(GameStates.GAME_PLAY)
        self.state_handler.start_game()
        self.assertNotEqual(self.state_handler.current_state, GameStates.BUILD_MODE)

if __name__ == '__main__':
    unittest.main()