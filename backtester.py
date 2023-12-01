from bbo import BBO
from direction import Direction
from open_order import Open_order
import matplotlib.pyplot as plt

def import_date(year, month, day):
    date_string = f"{year}-{month:02d}-{day:02d}"
    path = "data/" + date_string + ".txt"
    qr = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            qr.append(BBO.of_string(line.rstrip()))
    return list(reversed(qr))  # data is in reverse chronological order

class Backtester: 
    def __init__(self, quotes, cash):
        self.quotes = quotes
        self.cash = cash
        self.position = 0
        self.equity = cash
        self.open_order = None
        self.equity_over_time = []
        self.times = []
    
    def make_trade(self, direction, price, size, time):
        if direction == Direction.buy:
            self.cash -= size * price
            self.position += size
        elif direction == Direction.sell:
            self.cash += size * price
            self.position -= size
        self.update_equity(price, time)
        
    def update_equity(self, price, time):
        self.equity = self.cash + self.position * price
        self.equity_over_time.append(self.equity)
        self.times.append(time)
    
    def try_trade(self, quote):
        size = self.open_order.size
        price = self.open_order.price
        direction = self.open_order.direction
        if direction == Direction.buy and quote.get_ask_size() is not None:
            ask_size = quote.get_ask_size()
            ask_price = quote.get_ask_price()
            if price >= ask_price:
                trade_size = max(size, ask_size)
                self.make_trade(Direction.buy, ask_price, trade_size, quote.get_time())
                self.open_order = None
        if direction == Direction.sell and quote.get_bid_size() is not None:
            bid_size = quote.get_bid_size()
            bid_price = quote.get_bid_price()
            if price <= bid_price:
                trade_size = max(bid_size, size)
                self.make_trade(Direction.sell, bid_price, bid_size, quote.get_time())
                self.open_order = None

    def register_quote(self, quote):
        if quote.is_trade():
            self.update_equity(quote.get_mid_or_trade_price(), quote.get_time())
        elif quote.is_spread() and self.open_order is not None:
            self.try_trade(quote)
                
    def backtest(self, strategy):
        for i, quote in enumerate(self.quotes):
            print(
                    "loop progress:", f"{i / len(self.quotes) * 100:.2f}%", 
                    "equity:", f"{self.equity:.2f}", 
                    "position:", self.position, 
                    "            ",
                    end="\r"
                    )
            strategy.register_quote(quote)
            if strategy.wants_to_trade():
                size = strategy.trade_size
                price = strategy.trade_price
                direction: Direction = strategy.trade_direction
                self.open_order = Open_order(size, price, direction)
            self.register_quote(quote)
        plt.plot(self.times, self.equity_over_time)
        plt.show()

        

