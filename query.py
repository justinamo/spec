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

security = "SPY US Equity"

for day in range(2, 3):
    year = 2023
    month = 10
    day_of_week = date(year, month, day).weekday()

    if day_of_week > 4:
        continue

    day_ticks = []

    with open(f"data/{security}/{year}-{month:02d}-{day:02d}.txt", "w", encoding="utf-8") as file:
        for hour in range(10, 11):
            for min in range(0, 60, 5):
                request = IntradayTickRequest(service)
                request.set_security(security)
                request.add_field("TRADE")
                request.add_field("BID")
                request.add_field("ASK")
                start = datetime(year, month, day, hour, min, 0)
                request.set_start_time(start)
                if min + 5 == 60:
                    hour += 1
                    min = 0
                end = datetime(year, month, day, hour, min + 5, 0)
                request.set_end_time(end)
                request.include_detail()

                request.send(session)
                tick_data = extract_tick_data(session)
                ticks = list(map(Tick.of_tickdata_singleton, tick_data))
                day_ticks = day_ticks + ticks
                
                print("completed 5 mins")

        qrm = construct_qrm(day_ticks)
        for quote in qrm: 
            file.write(quote.__str__() + "\n")
        
    print(f"completed {year}-{month:02d}-{day:02d}")

session.stop()

event = session.tryNextEvent()
while event is not None:
    for message in event:
        print(message)
    event = session.tryNextEvent()