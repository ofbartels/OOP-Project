class CurrencyHandler:
    def __init__(self):
        self.currency = 1000

    def can_afford(self, amount):
        return self.currency >= amount

    def spend_currency(self, amount):
        if self.can_afford(amount):
            self.currency -= amount
            return True
        return False

    def add_currency(self, amount):
        self.currency += amount

    def get_currency(self):
        return self.currency
