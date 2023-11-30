from bbo import BBO
from direction import Direction

def import_date(year, month, day):
    date_string = f"{year}-{month:02d}-{day:02d}"
    path = "data/" + date_string + ".txt"
    qr = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            qr.append(BBO.of_string(line.rstrip()))
    return reversed(qr)  # data is in reverse chronological order

class Open_order:
    def __init__(self, size, price, direction):
        self.size = size
        self.price = price
        self.direction = direction

class Backtester: 
    def __init__(self, quotes, cash):
        self.quotes = quotes
        self.cash = cash
        self.position = 0
        self.equity = cash
        self.open_order = None
    
    def make_trade(self, direction, price, size):
        if direction == Direction.buy:
            self.cash -= size * price
            self.position += size
        elif direction == Direction.sell:
            self.cash += size * price
            self.position -= size
        self.update_equity(price)
        
    def update_equity(self, price):
        self.equity = self.cash + self.position * price
    
    def try_trade(self, quote):
        size = self.open_order.size
        price = self.open_order.price
        direction = self.open_order.direction
        if direction == Direction.buy and quote.ask_size is not None:
            ask_size = quote.ask_size
            ask_price = quote.ask_price
            if price >= ask_price:
                trade_size = max(size, ask_size)
                self.make_trade(Direction.buy, ask_price, trade_size)
                self.open_order = None
        if direction == Direction.sell and quote.bid_size is not None:
            bid_size = quote.bid_size
            bid_price = quote.bid_price
            if price <= bid_price:
                trade_size = max(bid_size, size)
                self.make_trade(Direction.sell, bid_price, bid_size)
                self.open_order = None

    def register_quote(self, quote):
        if quote.is_trade():
            self.update_equity(quote.price)
        elif quote.is_spread() and self.open_order is not None:
            self.try_trade(quote)
                
    def backtest(self, strategy):
        for quote in self.quotes:
            strategy.register_quote(quote)
            if strategy.wants_to_trade:
                size = strategy.trade_size
                price = strategy.trade_price
                direction: Direction = strategy.direction
                self.open_order = Open_order(size, price, direction)
            self.register_quote(quote)
        
        

                    






                


     

if __name__ == "__main__":
    import_date(2023, 10, 2)

