from datetime import datetime


def metro_service_status():

    now = datetime.now()

    current_time = now.hour + now.minute / 60

    start_time = 6
    end_time = 23

    if start_time <= current_time <= end_time:
        return True

    return False