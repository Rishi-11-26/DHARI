from datetime import datetime, timedelta

def metro_service_status():
    """
    Checks if the metro is currently operational (IST Time).
    Operating hours: 06:00 AM – 11:00 PM
    """
    # Servers (like Render) use UTC time. 
    # We add 5 hours and 30 minutes to convert UTC to Indian Standard Time (IST).
    now_utc = datetime.utcnow()
    now_ist = now_utc + timedelta(hours=5, minutes=30)

    current_time = now_ist.hour + now_ist.minute / 60

    start_time = 6.0   # 06:00 AM
    end_time = 23.0    # 11:00 PM

    if start_time <= current_time <= end_time:
        return True

    return False
