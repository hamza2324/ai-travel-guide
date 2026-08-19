from __future__ import annotations

import asyncio
import hashlib
from typing import Any

import httpx

from ..config import get_settings
from ..schemas.trip import Place
from ..utils.cache import places_cache
from .fallback_places import curated_for
from .geocoding_service import wikipedia_image
from .recommendation_service import category_from_tags, duration_for
from .fallback_places import curated_for

USER_AGENT = "AITravelGuide/1.0 (portfolio travel planner; local-dev)"

INTEREST_OVERPASS: dict[str, list[str]] = {
    "mountains": [
        'nwr["tourism"="viewpoint"]',
        'nwr["natural"="peak"]',
        'nwr["natural"="ridge"]',
    ],
    "nature": [
        'nwr["leisure"="park"]',
        'nwr["leisure"="nature_reserve"]',
        'nwr["tourism"="viewpoint"]',
        'nwr["natural"="water"]',
    ],
    "food": [
        'nwr["amenity"="restaurant"]',
        'nwr["amenity"="cafe"]',
        'nwr["amenity"="marketplace"]',
    ],
    "photography": [
        'nwr["tourism"="viewpoint"]',
        'nwr["tourism"="attraction"]',
        'nwr["historic"]',
    ],
    "history": [
        'nwr["historic"]',
        'nwr["tourism"="museum"]',
        'nwr["amenity"="place_of_worship"]',
    ],
    "culture": [
        'nwr["tourism"="museum"]',
        'nwr["tourism"="gallery"]',
        'nwr["amenity"="place_of_worship"]',
        'nwr["historic"="monument"]',
    ],
    "adventure": [
        'nwr["tourism"="attraction"]',
        'nwr["sport"]',
        'nwr["leisure"="nature_reserve"]',
    ],
    "shopping": [
        'nwr["shop"="mall"]',
        'nwr["amenity"="marketplace"]',
        'nwr["shop"="department_store"]',
    ],
    "relaxation": [
        'nwr["leisure"="park"]',
        'nwr["amenity"="cafe"]',
        'nwr["leisure"="garden"]',
    ],
    "beaches": [
        'nwr["natural"="beach"]',
        'nwr["leisure"="beach_resort"]',
    ],
    "wildlife": [
        'nwr["tourism"="zoo"]',
        'nwr["leisure"="nature_reserve"]',
        'nwr["tourism"="wildlife_park"]',
    ],
    "nightlife": [
        'nwr["amenity"="bar"]',
        'nwr["amenity"="pub"]',
        'nwr["amenity"="nightclub"]',
    ],
}

ALWAYS_QUERY = [
    'nwr["tourism"="attraction"]',
    'nwr["tourism"="viewpoint"]',
    'nwr["tourism"="museum"]',
    'nwr["historic"="monument"]',
    'nwr["leisure"="park"]',
    'nwr["tourism"="hotel"]',
]


def _cache_key(*parts: str) -> str:
    return hashlib.sha256("|".join(parts).encode()).hexdigest()


async def discover_places(
    lat: float,
    lng: float,
    interests: list[str],
    radius_km: int,
    travel_style: str = "balanced",
    destination: str = "",
) -> tuple[list[Place], str]:
    settings = get_settings()
    key = _cache_key("places", f"{lat:.3f}", f"{lng:.3f}", ",".join(sorted(interests)), str(radius_km), destination.lower())
    if key in places_cache:
        return places_cache[key]

    source = "openstreetmap"
    places: list[Place] = []
    try:
        if settings.google_enabled:
            places = await _discover_google(lat, lng, interests, radius_km, travel_style, settings.google_maps_api_key)
            source = "google"
        else:
            places = await _discover_overpass(lat, lng, interests, radius_km, travel_style)
            source = "openstreetmap"
    except Exception:
        places = []
        source = "curated"

    curated = curated_for(destination)
    seen = {place.name.lower() for place in places}
    for place in curated:
        if place.name.lower() not in seen:
            places.append(place)
            seen.add(place.name.lower())
    if curated and len(places) <= len(curated) + 2:
        source = f"{source}+curated"

    places = await _enrich_photos(places[:48])
    result = (places, source)
    places_cache[key] = result
    return result


async def _discover_overpass(
    lat: float, lng: float, interests: list[str], radius_km: int, travel_style: str
) -> list[Place]:
    radius_m = int(radius_km * 1000)
    filters: list[str] = list(ALWAYS_QUERY)
    for interest in interests:
        filters.extend(INTEREST_OVERPASS.get(interest, []))
    unique_filters = list(dict.fromkeys(filters))
    clauses = "\n".join(f'{flt}(around:{radius_m},{lat},{lng});' for flt in unique_filters)
    query = f"""
    [out:json][timeout:28];
    (
      {clauses}
    );
    out center tags 80;
    """
    endpoints = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
    ]
    data: dict[str, Any] = {}
    last_error: Exception | None = None
    for url in endpoints:
        try:
            async with httpx.AsyncClient(timeout=32, headers={"User-Agent": USER_AGENT}) as client:
                response = await client.post(url, data={"data": query})
                response.raise_for_status()
                data = response.json()
                break
        except httpx.HTTPError as exc:
            last_error = exc
            continue
    if not data:
        if last_error:
            raise last_error
        return []

    places: list[Place] = []
    seen: set[str] = set()
    for element in data.get("elements", []):
        tags = element.get("tags") or {}
        name = tags.get("name")
        if not name:
            continue
        el_lat = element.get("lat") or (element.get("center") or {}).get("lat")
        el_lng = element.get("lon") or (element.get("center") or {}).get("lon")
        if el_lat is None or el_lng is None:
            continue
        place_id = f"osm-{element.get('type')}-{element.get('id')}"
        if name.lower() in seen:
            continue
        seen.add(name.lower())
        category = category_from_tags(tags)
        extra_tags = [value for key, value in tags.items() if key in {"tourism", "historic", "leisure", "natural", "amenity"}]
        rating = _pseudo_rating(tags)
        address = tags.get("addr:full") or ", ".join(
            part for part in [tags.get("addr:street"), tags.get("addr:city")] if part
        )
        hours = tags.get("opening_hours")
        places.append(
            Place(
                id=place_id,
                name=name,
                category=category,
                lat=float(el_lat),
                lng=float(el_lng),
                rating=rating,
                user_ratings_total=int(tags.get("wikidata") is not None) * 40 + 12,
                address=address or None,
                opening_hours=[hours] if hours else None,
                estimated_duration_minutes=duration_for(category, travel_style),  # type: ignore[arg-type]
                tags=list({category, *extra_tags}),
                source="openstreetmap",
                wikipedia_url=f"https://en.wikipedia.org/wiki/{tags['wikipedia'].split(':', 1)[-1]}"
                if tags.get("wikipedia")
                else None,
            )
        )
    return places


GOOGLE_TYPE_MAP = {
    "mountains": ["tourist_attraction", "park"],
    "nature": ["park", "campground", "zoo"],
    "food": ["restaurant", "cafe"],
    "photography": ["tourist_attraction", "art_gallery"],
    "history": ["museum", "church", "hindu_temple", "mosque"],
    "culture": ["museum", "art_gallery", "church"],
    "adventure": ["amusement_park", "tourist_attraction"],
    "shopping": ["shopping_mall", "department_store"],
    "relaxation": ["spa", "park", "cafe"],
    "beaches": ["tourist_attraction"],
    "wildlife": ["zoo", "aquarium"],
    "nightlife": ["night_club", "bar"],
}


async def _discover_google(
    lat: float, lng: float, interests: list[str], radius_km: int, travel_style: str, api_key: str
) -> list[Place]:
    types: list[str] = ["tourist_attraction", "museum", "park", "restaurant", "lodging"]
    for interest in interests:
        types.extend(GOOGLE_TYPE_MAP.get(interest, []))
    unique_types = list(dict.fromkeys(types))[:8]
    places: list[Place] = []
    seen: set[str] = set()
    async with httpx.AsyncClient(timeout=14) as client:
        for place_type in unique_types:
            response = await client.get(
                "https://maps.googleapis.com/maps/api/place/nearbysearch/json",
                params={
                    "location": f"{lat},{lng}",
                    "radius": min(50000, radius_km * 1000),
                    "type": place_type,
                    "key": api_key,
                },
            )
            data = response.json()
            for item in data.get("results") or []:
                place_id = item.get("place_id")
                if not place_id or place_id in seen:
                    continue
                seen.add(place_id)
                loc = item["geometry"]["location"]
                types_list = item.get("types") or []
                category = _google_category(types_list)
                photo_ref = (item.get("photos") or [{}])[0].get("photo_reference")
                photo_url = (
                    f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photo_reference={photo_ref}&key={api_key}"
                    if photo_ref
                    else None
                )
                # Photo URLs with API keys must not be sent to the browser.
                # We keep the reference internally only; frontend uses category imagery / wikipedia.
                places.append(
                    Place(
                        id=f"g-{place_id}",
                        name=item.get("name", "Place"),
                        category=category,
                        lat=loc["lat"],
                        lng=loc["lng"],
                        rating=item.get("rating"),
                        user_ratings_total=item.get("user_ratings_total"),
                        address=item.get("vicinity"),
                        photo_url=None if photo_ref else None,
                        estimated_duration_minutes=duration_for(category, travel_style),  # type: ignore[arg-type]
                        tags=types_list[:6],
                        price_level=item.get("price_level"),
                        source="google",
                    )
                )
    return places


def _google_category(types_list: list[str]) -> str:
    mapping = {
        "museum": "museum",
        "art_gallery": "museum",
        "park": "park",
        "church": "religious",
        "mosque": "religious",
        "hindu_temple": "religious",
        "restaurant": "restaurant",
        "cafe": "cafe",
        "bar": "nightlife",
        "night_club": "nightlife",
        "shopping_mall": "shopping",
        "lodging": "hotel",
        "zoo": "wildlife",
        "spa": "spa",
        "natural_feature": "nature",
        "tourist_attraction": "attraction",
    }
    for item in types_list:
        if item in mapping:
            return mapping[item]
    return "attraction"


def _pseudo_rating(tags: dict[str, str]) -> float:
    score = 4.1
    if tags.get("wikidata") or tags.get("wikipedia"):
        score += 0.35
    if tags.get("tourism") == "attraction":
        score += 0.1
    if tags.get("historic"):
        score += 0.15
    if tags.get("opening_hours"):
        score += 0.05
    return round(min(4.9, score), 1)


async def _enrich_photos(places: list[Place]) -> list[Place]:
    async def hydrate(place: Place) -> Place:
        if place.photo_url:
            return place
        photo, extract = await wikipedia_image(place.name)
        if photo:
            place.photo_url = photo
        if extract and not place.description:
            place.description = extract[:280]
        return place

    head = await asyncio.gather(*(hydrate(place) for place in places[:8]))
    return [*head, *places[8:]]
