import blpapi
from dates import convert_to_utc

class IntradayTickRequest:
    def __init__(self, service):
        self.requestType = "IntradayTickRequest"
        self.request = service.createRequest(self.requestType)
    
    def set_security(self, bloombergTicker):
        self.request.set("security", bloombergTicker)
    
    def add_field(self, field):
        self.request.append("eventTypes", field)
    
    def include_detail(self):
        self.request.set("includeConditionCodes", True)
        self.request.set("includeExchangeCodes", True)
        self.request.set("includeTradeTime", True)
        self.request.set("includeNonPlottableEvents", True)
    
    def set_start_time(self, year, month, day, hour, minute, second):
        self.request.set(
            "startDateTime", 
            convert_to_utc(
                year, month, day, hour, minute, second
            )
        )

    def set_end_time(self, year, month, day, hour, minute, second):
        self.request.set(
            "endDateTime", 
            convert_to_utc(
                year, month, day, hour, minute, second
            )
        )
    
    def send(self, session):
        session.sendRequest(self.request)