import unittest
from unittest.mock import MagicMock
from madmasfrrse.handlers.event_handler import EventHandler

class TestEventHandler(unittest.TestCase):
    def setUp(self):
        """Setup for EventHandler tests."""
        self.event_handler = EventHandler()

    def test_initial_state(self):
        """Test the initial state of the event handler."""
        self.assertIsNotNone(self.event_handler.state)
        self.assertEqual(self.event_handler.state, 'INITIAL')  # Assuming default state is 'INITIAL'

    def test_handle_user_input(self):
        """Test handling user input."""
        user_input = {'key': 'space', 'action': 'pressed'}
        result = self.event_handler.handle_input(user_input)
        self.assertTrue(result)
        self.assertEqual(self.event_handler.last_input, user_input)

    def test_change_state(self):
        """Test changing states in the event handler."""
        self.event_handler.change_state('PAUSED')
        self.assertEqual(self.event_handler.state, 'PAUSED')

    def test_event_processing(self):
        """Test processing of a generic event."""
        mock_event = MagicMock()
        self.event_handler.process_event(mock_event)
        mock_event.process.assert_called_once()

if __name__ == '__main__':
    unittest.main()