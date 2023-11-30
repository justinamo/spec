from statistics import mean, stdev
from datetime import timedelta
from direction import Direction

class Strategy:
    def __init__(self): 
        self.quotes = []
        self.trade_size = None
        self.trade_price = None
        self.trade_direction = None
    
    def analyze_quotes(self):
        prices = list(map(lambda t: t.get_mid_or_trade_price(), self.quotes))
        avg_price = mean(prices)
        std = stdev(prices)
        last_price = prices[-1]

        z_score = (last_price - avg_price) / std
             
        return z_score

    def register_quote(self, quote):
        time = quote.get_time()
        self.quotes.append(quote)
        while time - self.quotes[0].get_time() > timedelta(minutes=5):
            del self.quotes[0]
        
    def wants_to_trade(self):
        if self.quotes[-1].get_time() - self.quotes[0].get_time() > timedelta(minutes=3):
            z_score = self.analyze_quotes()

            if self.quotes[-1].is_spread():
                if z_score < 1 and z_score > -1:
                    pass
                elif (z_score > 1 and z_score < 2) or z_score < -2:
                    self.trade_size = self.quotes[-1].get_bid_size()
                    self.trade_price = self.quotes[-1].get_bid_price()
                    self.trade_direction = Direction.sell
                    return True
                elif (z_score < -1 and z_score > -2) or z_score > 2:
                    self.trade_size = self.quotes[-1].get_ask_size()
                    self.trade_price = self.quotes[-1].get_ask_price()
                    self.trade_direction = Direction.buy
                    return True
        return False

