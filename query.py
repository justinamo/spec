'''
Requires a connection to the Bloomberg API. 
'''

import blpapi
from request import IntradayTickRequest
from eventParser import extract_tick_data
from tick import Tick, Tick_types


session = blpapi.Session()
session.start()

session.openService("//blp/refdata")
service = session.getService("//blp/refdata")

request = IntradayTickRequest(service)
request.set_security("IBM US Equity")
request.add_field("TRADE")
request.add_field("BID")
request.add_field("ASK")
request.set_start_time(2023, 11, 22, 10, 0, 0)
request.set_end_time(2023, 11, 22, 10, 0, 3)
request.include_detail()

request.send(session)
tick_data = extract_tick_data(session)
ticks = list(map(Tick.of_tickdata_singleton, tick_data))

qr = []
recent_bbo = {"BID": None, "ASK": None}
last = None
before_last = None
completed_pair = False

for tick in ticks: 
    popped_last_was_set = False
    tmp = last
    print(tick)
    if tick.type == Tick_types.trade:
        qr.append({"trade": tick})
        last = "TRADE"
    elif tick.type == Tick_types.bid:
        recent_bbo["BID"] = tick
        if recent_bbo["ASK"] is not None:
            if last == "ASK" and not popped_last and not before_last == "TRADE":
                qr.pop()
                popped_last = True
                popped_last_was_set = True
            qr.append(recent_bbo.copy())
            if not popped_last_was_set:
                popped_last = False
        last = "BID"
    elif tick.type == Tick_types.ask:
        recent_bbo["ASK"] = tick
        if recent_bbo["BID"] is not None:
            if last == "BID" and not popped_last and not before_last == "TRADE":
                qr.pop()
                popped_last = True
                popped_last_was_set = True
            qr.append(recent_bbo.copy())
            if not popped_last_was_set:
                popped_last = False
        last = "ASK"
    before_last = tmp

for quote in qr:
    print(quote)
        
session.stop()