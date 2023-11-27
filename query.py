'''
Requires a connection to the Bloomberg API. 
'''

import blpapi
from request import IntradayTickRequest
from event_parser import extract_tick_data, construct_qrm
from tick import Tick
from datetime import datetime


session = blpapi.Session()
session.start()

session.openService("//blp/refdata")
service = session.getService("//blp/refdata")

request = IntradayTickRequest(service)
request.set_security("IBM US Equity")
request.add_field("TRADE")
request.add_field("BID")
request.add_field("ASK")
start = datetime(2023, 11, 22, 10, 0, 0)
request.set_start_time(start)
end = datetime(2023, 11, 22, 15, 30, 0)
request.set_end_time(end)
request.include_detail()

request.send(session)
tick_data = extract_tick_data(session)
ticks = list(map(Tick.of_tickdata_singleton, tick_data))
qrm = construct_qrm(ticks)



session.stop()