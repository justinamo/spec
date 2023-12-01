from portfolio import Portfolio
from position import Position
from backtester import Backtester

class Portfolio_backtester:
    def __init__(self):
        self.portfolio = Portfolio()
        self.backtests = {}

    def add_security(self, bloomberg, quotes):
        position = Position(bloomberg)
        portfolio.add_position(position)
        backtests[bloomberg] = Backtester(quotes, 0)

    def get_portfolio_cash(self): 
        net_cash = 0
        for bloomberg in self.backtests: 
            net_cash += self.backtests[bloomberg].cash

    def get_portfolio_equity(self): 
        for 
