class CurrencyHandler:
    def __init__(self):
        self.currency = 1000
        self.wood = 100
        self.stone = 10
        self.iron = 0
        self.magica = 0

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
