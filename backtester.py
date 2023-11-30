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

    def backtest(self, strategy):
        for quote in self.quotes:
            strategy.register_quote(quote)

            if strategy.wants_to_trade:
                size = strategy.trade_size
                price = strategy.trade_price
                direction: Direction = strategy.direction
                self.open_order = { "size": size, "price": price, "direction": direction }
                if quote.is_spread:
                    if direction == Direction.buy:
                        ask_size = quote.ask_size
                        ask_price = quote.ask_price
                        if price >= ask_price:
                            trade_size = max(size, ask_size)
                            self.position += trade_size
                            self.cash -= trade_size * ask_price






                


     

if __name__ == "__main__":
    import_date(2023, 10, 2)

