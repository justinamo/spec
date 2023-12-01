class Portfolio: 
    def __init__(self):
        self.positions = {}

    def add_position(self, position):
        if position.ticker in self.positions:
            self.positions[position.ticker] += position
        else:
            self.positions[position.ticker] = position

    def get_tickers(self):
        return list(self.positions.keys())

    def get_position(self, bloomberg):
        return self.positions[bloomberg]


