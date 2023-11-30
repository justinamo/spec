import blpapi
from dates import convert_from_utc
from tick_types import Tick_types

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

        eastern_time = convert_from_utc(time)

        if tick_type == Tick_types.bid or tick_type == Tick_types.ask:
            size *= 100

        return Tick(eastern_time, tick_type, price, size, exch_code)