import blpapi
from tick import Tick_types
from dates import convert_from_utc
from bbo import BBO

tickData = blpapi.Name("tickData")

def extract_tick_data(session):
    while session.tryNextEvent():
        event = session.nextEvent()
        for message in event:
            if message.hasElement(tickData):
                td = message.asElement().getElement(tickData)
                return td.getElement(tickData)

def construct_qrm(ticks):

    qr = []
    recent_bbo = {"BID": None, "ASK": None}
    last = None

    for tick in ticks:
        if tick.type == Tick_types.trade:
            qr.append({"TRADE": tick})
        elif tick.type == Tick_types.bid:
            recent_bbo["BID"] = tick
            qr.append(recent_bbo.copy())
        elif tick.type == Tick_types.ask:
            recent_bbo["ASK"] = tick
            qr.append(recent_bbo.copy())
            
    ticks.reverse()
    qr.reverse()

    last_deleted = None

    to_delete = []
    for i in range(len(ticks)):
        last_deleted_was_set = False
        if ticks[i].type != Tick_types.trade and ticks[i-1].type != Tick_types.trade:
            if ticks[i-1].type != ticks[i].type and not last_deleted:
                to_delete.append(i)
                last_deleted = True
                last_deleted_was_set = True
            if not last_deleted_was_set:
                last_deleted = False

    to_delete.reverse()

    for i in to_delete:
        del qr[i]

    def construct_bbo(quote):
        if "TRADE" in quote: 
            return BBO("TRADE", quote)
        else:
            return BBO("SPREAD", quote)

    return list(map(construct_bbo, qr))

            