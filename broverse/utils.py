from datetime import datetime, timezone

def get_timestamp():
    dt = datetime.now(timezone.utc)
    return dt.isoformat()