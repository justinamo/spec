'''
Requires a connection to the Bloomberg API. 
'''

import blpapi
from request import IntradayTickRequest
from event_parser import extract_tick_data, construct_qrm
from tick import Tick
from datetime import date, datetime


session = blpapi.Session()
session.start()

session.openService("//blp/refdata")
service = session.getService("//blp/refdata")

for day in range(1, 31):

    year = 2023
    month = 10

    day_of_week = date(year, month, day).weekday()

    if day_of_week > 4:
        continue

    request = IntradayTickRequest(service)
    request.set_security("IBM US Equity")
    request.add_field("TRADE")
    request.add_field("BID")
    request.add_field("ASK")
    start = datetime(year, month, day, 10, 0, 0)
    request.set_start_time(start)
    end = datetime(year, month, day, 15, 30, 0)
    request.set_end_time(end)
    request.include_detail()

    request.send(session)
    tick_data = extract_tick_data(session)
    ticks = list(map(Tick.of_tickdata_singleton, tick_data))
    qrm = construct_qrm(ticks)

    with open(f"data/{year}-{month:02d}-{day:02d}.txt", "w", encoding="utf-8") as file:
        for quote in qrm: 
            file.write(quote.__str__() + "\n")
    
    print(f"completed {year}-{month:02d}-{day:02d}")


session.stop()