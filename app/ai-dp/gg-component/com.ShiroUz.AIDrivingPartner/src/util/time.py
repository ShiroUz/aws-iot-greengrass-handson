import time
from datetime import datetime, timezone

def get_utc_time():
    """Get current UTC time as Unix timestamp"""
    return int(time.time())

def get_formatted_time():
    """Get current time formatted as string"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_iso_timestamp():
    """Get current time in ISO format"""
    return datetime.now(timezone.utc).isoformat()