import math
from utils.data_loader import load_stations

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculates distance between two coordinates in km."""
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (math.sin(dlat/2)**2 +
         math.cos(lat1) * math.cos(lat2) *
         math.sin(dlon/2)**2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def find_nearest_station(user_lat, user_lon):
    """Finds the closest metro station to user's location."""
    stations_df = load_stations()
    nearest_station = None
    min_distance = float("inf")

    for _, row in stations_df.iterrows():
        distance = haversine_distance(user_lat, user_lon, row["lat"], row["lon"])
        if distance < min_distance:
            min_distance = distance
            nearest_station = row["station"]

    return nearest_station, min_distance