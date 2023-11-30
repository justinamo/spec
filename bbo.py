from typing import Optional
from tick import Tick, Tick_types
from datetime import datetime

class BBO_Type: 
    trade = "TRADE"
    spread = "SPREAD"

class Trade: 
    def __init__(self, trade_tick: Tick):
        self.time = trade_tick.time
        self.price = trade_tick.price
        self.size = trade_tick.size
        self.exchange = trade_tick.exchange
    
    def __repr__(self):
        return " ".join([
            str(self.time), 
            "TRADE", 
            str(self.size), 
            str(self.price), 
            self.exchange
        ])
    
    def __str__(self):
        return " ".join([
            str(self.time), 
            "TRADE", 
            str(self.size), 
            str(self.price), 
            self.exchange
        ])
    

class Spread:
    def __init__(self, bid_tick: Optional[Tick], ask_tick: Optional[Tick]):
        if bid_tick is None:
            self.time = ask_tick.time
            self.bid_exchange = None
            self.bid_price = None
            self.bid_size = None
            self.ask_size = ask_tick.size
            self.ask_price = ask_tick.price
            self.ask_exchange = ask_tick.exchange
        elif ask_tick is None:
            self.time = bid_tick.time
            self.bid_exchange = bid_tick.exchange
            self.bid_price = bid_tick.price
            self.bid_size = bid_tick.size
            self.ask_size = None
            self.ask_price = None
            self.ask_exchange = None
        else:
            self.time = max(bid_tick.time, ask_tick.time)
            self.bid_exchange = bid_tick.exchange
            self.bid_price = bid_tick.price
            self.bid_size = bid_tick.size
            self.ask_size = ask_tick.size
            self.ask_price = ask_tick.price
            self.ask_exchange = ask_tick.exchange

    def __str__(self):
        return " ".join([
            str(self.time), 
            "BID", 
            str(self.bid_exchange), 
            str(self.bid_price),
            str(self.bid_size), 
            str(self.ask_size), 
            str(self.ask_price), 
            str(self.ask_exchange), 
            "ASK"
        ])

    def __repr__(self):
        return " ".join([
            str(self.time), 
            "BID", 
            str(self.bid_exchange), 
            str(self.bid_price),
            str(self.bid_size), 
            str(self.ask_size), 
            str(self.ask_price), 
            str(self.ask_exchange), 
            "ASK"
        ])


class BBO:
    def __init__(self, trade_or_spread, data):
        if trade_or_spread == "TRADE":
            self.type = BBO_Type.trade
            self.data = Trade(data["TRADE"])
        elif trade_or_spread == "SPREAD":
            self.type = BBO_Type.spread
            self.data = Spread(data["BID"], data["ASK"])
        else:
            raise Exception(f"Unsupported BBO type. Use 'trade' or 'spread'.")
    
    def __str__(self):
        return self.data.__str__()
        
    def __repr__(self):
        return self.data.__repr__()

    def is_spread(self):
        return self.type == BBO_Type.spread

    def is_trade(self):
        return self.type == BBO_Type.trade
    
    def get_mid_or_trade_price(self):
        if self.is_spread():
            if self.get_ask_price() == None:
                return self.get_bid_price()
            elif self.get_bid_price() == None:
                return self.get_ask_price()
            else:
                return (self.get_ask_price() + self.get_bid_price()) / 2
        elif self.is_trade():
            return self.data.price    
    
    def get_bid_size(self):
        if self.type == BBO_Type.spread:
            return self.data.bid_size
        else:
            raise("trying to get bid_size of Trade")

    def get_ask_size(self):
        if self.type == BBO_Type.spread:
            return self.data.ask_size
        else:
            raise("trying to get ask_size of Trade")
    
    def get_bid_price(self):
        if self.type == BBO_Type.spread:
            return self.data.bid_price
        else:
            raise("trying to get bid_price of Trade")

    def get_ask_price(self):
        if self.type == BBO_Type.spread:
            return self.data.ask_price
        else:
            raise("trying to get ask_price of Trade")
    
    def get_time(self):
        return self.data.time

    def of_string(string):
        fields = string.split()
        date = fields[0]
        time = fields[1]
        dt = datetime.fromisoformat(date + " " + time)
        trade_or_bid = fields[2]
        if trade_or_bid == Tick_types.trade:
            # TODO: decouple string representations for spread and trade
            #       and decouple BBO constructor from Tick
            size = int(fields[3])
            price = float(fields[4])
            exchange = fields[5]
            data = { "TRADE": Tick(dt, Tick_types.trade, price, size, exchange) }
            return BBO(BBO_Type.trade, data)
        else:
            bid_exchange = fields[3]
            bid_price = float(fields[4]) if fields[4] != "None" else None
            bid_size = int(fields[5]) if fields[5] != "None" else None
            ask_size = int(fields[6]) if fields[6] != "None" else None
            ask_price = float(fields[7]) if fields[7] != "None" else None
            ask_exchange = fields[8]
            data = {
                "BID": Tick(dt, Tick_types.bid, bid_price, bid_size, bid_exchange),
                "ASK": Tick(dt, Tick_types.ask, ask_price, ask_size, ask_exchange)
            }
            return BBO(BBO_Type.spread, data)


        
        
