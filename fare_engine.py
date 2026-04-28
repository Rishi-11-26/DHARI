from utils.data_loader import load_fares

def calculate_fare(distance):
    """Calculates fare based on distance slabs."""
    fare_df = load_fares()
    
    slab = fare_df[
        (fare_df["distance_km_min"] <= distance) &
        (fare_df["distance_km_max"] >= distance)
    ]

    if not slab.empty:
        return slab.iloc[0]["fare_inr"]

    return None