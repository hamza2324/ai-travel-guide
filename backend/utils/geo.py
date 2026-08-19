from math import atan2, cos, radians, sin, sqrt

EARTH_RADIUS_KM = 6371.0


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    rlat1, rlng1, rlat2, rlng2 = map(radians, [lat1, lng1, lat2, lng2])
    dlat = rlat2 - rlat1
    dlng = rlng2 - rlng1
    a = sin(dlat / 2) ** 2 + cos(rlat1) * cos(rlat2) * sin(dlng / 2) ** 2
    return EARTH_RADIUS_KM * 2 * atan2(sqrt(a), sqrt(1 - a))


def estimate_drive_minutes(distance_km: float) -> int:
    """Urban-biased driving estimate when live routing is unavailable."""
    if distance_km <= 0:
        return 0
    if distance_km < 1.5:
        return max(6, int(distance_km * 12))
    if distance_km < 8:
        return int(8 + distance_km * 3.4)
    return int(12 + distance_km * 2.1)


def radius_for_trip(duration_days: int, travel_style: str) -> int:
    base = 28 + duration_days * 14
    if travel_style == "relaxed":
        base = int(base * 0.85)
    elif travel_style == "fast-paced":
        base = int(base * 1.2)
    return min(160, max(22, base))
