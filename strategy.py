from statistics import mean, stdev
from datetime import timedelta

class Strategy:
    def __init__(self): 
        self.quotes = []
    
    def analyze_quotes(self):
        prices = list(map(lambda t: t.mid_or_trade_price(), self.quotes))
        avg_price = mean(prices)
        std = stdev(prices)
        last_price = prices[-1]

        z_score = (last_price - avg_price) / std
             
        return z_score

    def register_quote(self, quote):
        time = quote.get_time()
        quote = self.quotes[0]
        while time - self.quotes[0].get_time() > timedelta(minutes=5):
            del self.quotes[0]
        
    def wants_to_trade(self):
        z_score = self.analyze_quotes(self.quotes)

        if z_score < 1 and z_score > -1:
            pass
