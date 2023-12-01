class Position:
    def __init__(self, bloomberg):
        self.ticker = bloomberg
        self.position = 0

    def buy(self, quantity):
        self.position += quantity

    def sell(self, quantity):
        self.position -= quantity

