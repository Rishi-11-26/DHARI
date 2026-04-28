def estimate_travel(route):

    stations_travelled = len(route) - 1

    time_minutes = stations_travelled * 2

    return stations_travelled, time_minutes