import unittest
from unittest.mock import MagicMock
from madmasfrrse.handlers.ui_handler import UIManager
from madmasfrrse.handlers.currency_handler import CurrencyHandler
from madmasfrrse.handlers.event_handler import EventHandler
from madmasfrrse.handlers.state_handler import StateHandler, GameStates
from madmasfrrse.handlers.phase_handler import PhaseHandler

class TestUIManager(unittest.TestCase):
    def setUp(self):
        """Setup for UIManager tests."""
        self.screen = MagicMock()
        self.currency_handler = CurrencyHandler()
        self.event_handler = EventHandler()
        self.state_handler = StateHandler()
        self.phase_handler = PhaseHandler()
        self.ui_manager = UIManager(self.screen, self.currency_handler, self.event_handler, self.state_handler, self.phase_handler)

    def test_initialization(self):
        """Test UIManager initialization and component setup."""
        self.assertIsInstance(self.ui_manager.components, list)
        self.assertTrue(self.ui_manager.components)  # Check if components list is not empty

    def test_handle_event(self):
        """Test event handling by UI components."""
        mock_event = MagicMock()
        self.ui_manager.handle_event(mock_event)
        # Assuming the handle_event method processes the event through components
        # This would typically assert something about the event handling logic

    def test_update(self):
        """Test the update method refreshes UI based on game state."""
        # Simulate changes in currency and verify UI update
        initial_currency_display = self.ui_manager.currency_display.text
        self.currency_handler.add_currency(100)
        self.ui_manager.update()
        updated_currency_display = self.ui_manager.currency_display.text
        self.assertNotEqual(initial_currency_display, updated_currency_display)

    def test_draw(self):
        """Test drawing UI components."""
        self.ui_manager.draw()
        # Verify that the draw method of each UI component is called
        for component in self.ui_manager.components:
            component.draw.assert_called_with(self.screen)

if __name__ == '__main__':
    unittest.main()