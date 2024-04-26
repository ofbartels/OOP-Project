import unittest
from unittest.mock import MagicMock
from madmasfrrse.handlers.state_handler import GameStateHandler, GameStates
from madmasfrrse.handlers.ui_handler import UIManager
from madmasfrrse.handlers.event_handler import EventHandler
from madmasfrrse.handlers.phase_handler import PhaseHandler
from madmasfrrse.handlers.currency_handler import CurrencyHandler

class TestGameFlow(unittest.TestCase):
    def setUp(self):
        """Setup for Game Flow tests."""
        self.screen = MagicMock()
        self.currency_handler = CurrencyHandler()
        self.event_handler = EventHandler()
        self.state_handler = GameStateHandler()
        self.phase_handler = PhaseHandler()
        self.ui_manager = UIManager(self.screen, self.currency_handler, self.event_handler, self.state_handler, self.phase_handler)

    def test_start_game_flow(self):
        """Test the flow from game start through initial gameplay."""
        # Initial state should be at the start menu
        self.assertEqual(self.state_handler.current_state, GameStates.START_MENU)
        
        # Simulate starting the game which should change the state to BUILD_MODE
        self.ui_manager.handle_event('start_game')
        self.assertEqual(self.state_handler.current_state, GameStates.BUILD_MODE)
        
        # Simulate user triggering the next phase which should move to GAME_PLAY
        self.ui_manager.handle_event('play_button_pressed')
        self.assertEqual(self.state_handler.current_state, GameStates.GAME_PLAY)
        
        # Check if a wave is active
        self.assertTrue(self.phase_handler.phase_active)

    def test_game_pause_and_resume(self):
        """Test pausing and resuming the game."""
        # Start the game and move to gameplay
        self.ui_manager.handle_event('start_game')
        self.ui_manager.handle_event('play_button_pressed')
        self.assertEqual(self.state_handler.current_state, GameStates.GAME_PLAY)
        
        # Pause the game
        self.ui_manager.handle_event('pause_game')
        self.assertEqual(self.state_handler.current_state, GameStates.PAUSE)
        
        # Resume the game
        self.ui_manager.handle_event('resume_game')
        self.assertEqual(self.state_handler.current_state, GameStates.GAME_PLAY)

    def test_game_over_scenario(self):
        """Test handling of game over scenario."""
        # Assume game is in play
        self.ui_manager.handle_event('start_game')
        self.ui_manager.handle_event('play_button_pressed')
        
        # Trigger game over
        self.ui_manager.handle_event('game_over')
        self.assertEqual(self.state_handler.current_state, GameStates.GAME_OVER)

if __name__ == '__main__':
    unittest.main()