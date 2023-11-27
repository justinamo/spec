import pytz
from datetime import datetime
    
date_format = '%Y-%m-%dT%H:%M:%S'
eastern = pytz.timezone("US/Eastern")
utc = pytz.utc

def convert_to_utc(dt):
    eastern_time = eastern.localize(naive)
    utc_time = eastern_time.astimezone(utc)
    return utc_time.strftime(date_format)

def convert_from_utc(dt):
    utc_time = utc.localize(dt)
    eastern_time = utc_time.astimezone(eastern)
    return eastern_time
