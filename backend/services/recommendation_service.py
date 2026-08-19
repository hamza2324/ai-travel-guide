import math
from datetime import datetime, timedelta

from ..schemas.trip import Place, TravelStyle
from ..utils.geo import haversine_km

INTEREST_CATEGORY_WEIGHTS: dict[str, dict[str, float]] = {
    "mountains": {"viewpoint": 1.0, "nature": 0.85, "park": 0.7, "adventure": 0.65, "attraction": 0.4},
    "nature": {"park": 1.0, "nature": 1.0, "viewpoint": 0.85, "wildlife": 0.8, "beach": 0.6},
    "food": {"restaurant": 1.0, "cafe": 0.85, "market": 0.7, "attraction": 0.2},
    "photography": {"viewpoint": 1.0, "nature": 0.8, "historic": 0.7, "architecture": 0.75, "attraction": 0.55},
    "history": {"historic": 1.0, "museum": 0.9, "architecture": 0.75, "religious": 0.7, "attraction": 0.5},
    "culture": {"museum": 0.95, "historic": 0.8, "religious": 0.75, "market": 0.65, "attraction": 0.55},
    "adventure": {"adventure": 1.0, "nature": 0.7, "viewpoint": 0.65, "park": 0.55},
    "shopping": {"shopping": 1.0, "market": 0.9, "attraction": 0.2},
    "relaxation": {"park": 0.85, "cafe": 0.7, "spa": 0.9, "beach": 0.85, "viewpoint": 0.55, "nature": 0.6},
    "beaches": {"beach": 1.0, "nature": 0.5, "viewpoint": 0.4},
    "wildlife": {"wildlife": 1.0, "nature": 0.85, "park": 0.75},
    "nightlife": {"nightlife": 1.0, "restaurant": 0.45, "cafe": 0.3},
}

DURATION_BY_CATEGORY = {
    "viewpoint": 50,
    "museum": 100,
    "historic": 75,
    "religious": 60,
    "park": 80,
    "nature": 90,
    "restaurant": 75,
    "cafe": 45,
    "shopping": 70,
    "market": 55,
    "adventure": 120,
    "beach": 90,
    "wildlife": 100,
    "nightlife": 90,
    "hotel": 0,
    "spa": 80,
    "architecture": 60,
    "attraction": 70,
}

MEAL_CATEGORIES = {"restaurant", "cafe", "market"}
ATTRACTION_CATEGORIES = {
    "viewpoint",
    "museum",
    "historic",
    "religious",
    "park",
    "nature",
    "adventure",
    "beach",
    "wildlife",
    "architecture",
    "attraction",
    "shopping",
}


def category_from_tags(tags: dict[str, str] | None, fallback: str = "attraction") -> str:
    tags = tags or {}
    tourism = tags.get("tourism", "")
    historic = tags.get("historic")
    leisure = tags.get("leisure", "")
    amenity = tags.get("amenity", "")
    natural = tags.get("natural", "")
    shop = tags.get("shop")

    if tourism in {"viewpoint", "museum", "gallery", "hotel", "attraction", "theme_park", "zoo"}:
        mapping = {
            "viewpoint": "viewpoint",
            "museum": "museum",
            "gallery": "museum",
            "hotel": "hotel",
            "theme_park": "adventure",
            "zoo": "wildlife",
            "attraction": "attraction",
        }
        return mapping.get(tourism, "attraction")
    if historic:
        return "historic"
    if leisure in {"park", "nature_reserve", "garden"}:
        return "park"
    if amenity in {"place_of_worship"}:
        return "religious"
    if amenity in {"restaurant", "fast_food"}:
        return "restaurant"
    if amenity in {"cafe", "tea_house"}:
        return "cafe"
    if amenity in {"bar", "pub", "nightclub"}:
        return "nightlife"
    if natural in {"peak", "ridge", "cliff", "beach", "wood", "water", "lake"}:
        return "beach" if natural == "beach" else "nature"
    if shop:
        return "shopping"
    if tourism == "picnic_site":
        return "park"
    return fallback


def interest_match(category: str, interests: list[str], tags: list[str] | None = None) -> float:
    score = 0.0
    haystack = {category, *(tags or [])}
    for interest in interests:
        weights = INTEREST_CATEGORY_WEIGHTS.get(interest, {})
        best = 0.0
        for key, weight in weights.items():
            if key in haystack or key == category:
                best = max(best, weight)
        score += best
    if not interests:
        return 0.4
    return min(1.0, score / max(1, len(interests)))


def rating_score(rating: float | None, count: int | None) -> float:
    if rating is None:
        return 0.45
    base = max(0.0, min(1.0, (rating - 2.8) / 2.2))
    confidence = 0.55 + min(0.45, math.log10(max(count or 1, 1) + 1) / 4)
    return base * confidence


def distance_score(distance_km: float, radius_km: float) -> float:
    if distance_km <= 2:
        return 1.0
    ratio = distance_km / max(radius_km, 1)
    return max(0.05, 1.0 - min(1.0, ratio * 0.85))


def budget_score(category: str, price_level: int | None, budget: str) -> float:
    if price_level is None:
        return 0.72
    if budget == "budget":
        return {0: 1.0, 1: 0.95, 2: 0.55, 3: 0.2, 4: 0.05}.get(price_level, 0.6)
    if budget == "premium":
        return {0: 0.45, 1: 0.55, 2: 0.8, 3: 1.0, 4: 1.0}.get(price_level, 0.75)
    return {0: 0.7, 1: 0.85, 2: 1.0, 3: 0.7, 4: 0.35}.get(price_level, 0.75)


def itinerary_fit_score(category: str, travel_style: TravelStyle) -> float:
    if travel_style == "relaxed" and category in {"adventure", "shopping", "nightlife"}:
        return 0.55
    if travel_style == "fast-paced" and category in {"museum", "spa"}:
        return 0.7
    if travel_style == "relaxed" and category in {"park", "cafe", "viewpoint", "nature"}:
        return 1.0
    return 0.85


def compute_match_score(
    place: Place,
    interests: list[str],
    budget: str,
    travel_style: TravelStyle,
    origin_lat: float,
    origin_lng: float,
    radius_km: float,
) -> tuple[float, list[str]]:
    dist = haversine_km(origin_lat, origin_lng, place.lat, place.lng)
    i_score = interest_match(place.category, interests, place.tags)
    r_score = rating_score(place.rating, place.user_ratings_total)
    d_score = distance_score(dist, radius_km)
    b_score = budget_score(place.category, place.price_level, budget)
    f_score = itinerary_fit_score(place.category, travel_style)

    total = (
        i_score * 34
        + r_score * 22
        + d_score * 16
        + b_score * 10
        + f_score * 10
        + min(8.0, (place.user_ratings_total or 0) / 80)
    )
    total = max(12.0, min(99.0, total))

    reasons = []
    if i_score >= 0.7:
        reasons.append("strongly matches your interests")
    elif i_score >= 0.4:
        reasons.append("fits several of your interests")
    if place.rating and place.rating >= 4.4:
        reasons.append("has excellent visitor ratings")
    elif place.rating and place.rating >= 4.0:
        reasons.append("is well reviewed")
    if dist <= 8:
        reasons.append("is conveniently close to your route")
    if f_score >= 0.9:
        reasons.append("suits your travel pace")
    return round(total, 1), reasons[:3]


def duration_for(category: str, travel_style: TravelStyle) -> int:
    base = DURATION_BY_CATEGORY.get(category, 70)
    if travel_style == "relaxed":
        return int(base * 1.25)
    if travel_style == "fast-paced":
        return int(base * 0.8)
    return base


def parse_clock(value: str) -> datetime:
    return datetime.strptime(value, "%H:%M")


def format_clock(value: datetime) -> str:
    return value.strftime("%H:%M")


def add_minutes(clock: str, minutes: int) -> str:
    dt = parse_clock(clock) + timedelta(minutes=minutes)
    return format_clock(dt)


def day_window(travel_style: TravelStyle) -> tuple[str, str, int]:
    if travel_style == "relaxed":
        return "09:30", "18:30", 3
    if travel_style == "fast-paced":
        return "08:00", "21:00", 6
    return "09:00", "20:00", 4
