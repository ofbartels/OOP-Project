import unittest
from madmasfrrse.handlers.currency_handler import CurrencyHandler

class TestCurrencyHandler(unittest.TestCase):
    def setUp(self):
        """Setup for CurrencyHandler tests."""
        self.currency_handler = CurrencyHandler()

    def test_initial_currency(self):
        """Test the initial amount of currency."""
        self.assertEqual(self.currency_handler.get_currency(), 1000)
        self.assertEqual(self.currency_handler.wood, 100)
        self.assertEqual(self.currency_handler.stone, 10)
        self.assertEqual(self.currency_handler.iron, 0)
        self.assertEqual(self.currency_handler.magica, 0)

    def test_can_afford(self):
        """Test if the can_afford method returns correctly based on currency amount."""
        self.assertTrue(self.currency_handler.can_afford(500))
        self.assertFalse(self.currency_handler.can_afford(1500))

    def test_spend_currency(self):
        """Test spending currency reduces the amount correctly."""
        result = self.currency_handler.spend_currency(500)
        self.assertTrue(result)
        self.assertEqual(self.currency_handler.get_currency(), 500)
        # Test failing to spend currency that isn't affordable
        result = self.currency_handler.spend_currency(600)
        self.assertFalse(result)
        self.assertEqual(self.currency_handler.get_currency(), 500)

    def test_add_currency(self):
        """Test adding currency."""
        self.currency_handler.add_currency(500)
        self.assertEqual(self.currency_handler.get_currency(), 1500)

if __name__ == '__main__':
    unittest.main()