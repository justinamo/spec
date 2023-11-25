import blpapi

class Tick_types:
    bid = "BID"
    ask = "ASK"
    trade = "TRADE"

class Tick:
    def __init__(self, time, tick_type, price, size, exchange):
        self.time = time
        self.type = tick_type
        self.price = price
        self.size = size
        self.exchange = exchange

    def __str__(self):
        return (
            str(self.time) + " " 
            + self.type + " " 
            + str(self.price) + " " 
            + str(self.size) + " " 
            + self.exchange
        )

    def __repr__(self):
        return (
            str(self.time) + " " 
            + self.type + " " 
            + str(self.price) + " " 
            + str(self.size) + " " 
            + self.exchange
        )

    def of_tickdata_singleton(singleton):
        time = singleton.getElementAsDatetime(blpapi.Name("time"))
        tick_type = singleton.getElementAsString(blpapi.Name("type"))
        price = singleton.getElementAsFloat(blpapi.Name("value"))
        size = singleton.getElementAsInteger(blpapi.Name("size"))
        exch_code = singleton.getElementAsString(blpapi.Name("exchangeCode"))

        return Tick(time, tick_type, price, size, exch_code)