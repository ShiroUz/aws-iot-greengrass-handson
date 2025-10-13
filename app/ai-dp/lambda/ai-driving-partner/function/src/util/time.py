import time
from datetime import datetime, timezone

# TTL 3 months(60sec, 60min, 24h, 90day)
EXPIRE_TIME = 60 * 60 * 24 * 90

def get_utc_time():
    return int(time.time())

def get_expiration_time():
    return int(time.time()) + EXPIRE_TIME

def unix_to_utc_string(unix_timestamp_str):
    return datetime.fromtimestamp(int(unix_timestamp_str), tz=timezone.utc).strftime('%Y/%m/%d/%H/%M/%S')
