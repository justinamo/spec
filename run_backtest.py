from backtester import Backtester, import_date
from strategy import Strategy

quotes = import_date(2023, 10, 2)

bt = Backtester(quotes, 1000000)

strat = Strategy()

bt.backtest(strat)

print(bt.cash, bt.position, bt.equity)
