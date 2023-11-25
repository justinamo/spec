import blpapi
from dates import convert_from_utc

tickData = blpapi.Name("tickData")

def extract_tick_data(session):
    while session.tryNextEvent():
        event = session.nextEvent()
        for message in event:
            if message.hasElement(tickData):
                td = message.asElement().getElement(tickData)
                return td.getElement(tickData)

def construct_qrm(tick_data):
    return

            