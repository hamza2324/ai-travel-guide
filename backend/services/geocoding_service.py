from __future__ import annotations

import hashlib
from urllib.parse import quote

import httpx

from ..config import get_settings
from ..schemas.trip import GeoPoint
from ..utils.cache import geocode_cache, wiki_cache
from ..utils.errors import LocationNotFoundError

USER_AGENT = "AITravelGuide/1.0 (portfolio travel planner; local-dev)"


def _cache_key(*parts: str) -> str:
    return hashlib.sha256("|".join(parts).encode()).hexdigest()


async def geocode(query: str) -> GeoPoint:
    settings = get_settings()
    key = _cache_key("geocode", query.lower(), "google" if settings.google_enabled else "osm")
    if key in geocode_cache:
        return geocode_cache[key]

    if settings.google_enabled:
        point = await _geocode_google(query, settings.google_maps_api_key)
    else:
        point = await _geocode_nominatim(query)

    if not point:
        raise LocationNotFoundError(query)
    geocode_cache[key] = point
    return point


async def reverse_geocode(lat: float, lng: float) -> str:
    key = _cache_key("reverse", f"{lat:.4f}", f"{lng:.4f}")
    if key in geocode_cache:
        return geocode_cache[key]

    settings = get_settings()
    label = None
    if settings.google_enabled:
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.get(
                "https://maps.googleapis.com/maps/api/geocode/json",
                params={"latlng": f"{lat},{lng}", "key": settings.google_maps_api_key},
            )
            data = response.json()
            results = data.get("results") or []
            if results:
                label = results[0].get("formatted_address")
    if not label:
        async with httpx.AsyncClient(timeout=12, headers={"User-Agent": USER_AGENT}) as client:
            response = await client.get(
                "https://nominatim.openstreetmap.org/reverse",
                params={"lat": lat, "lon": lng, "format": "jsonv2"},
            )
            data = response.json()
            address = data.get("address") or {}
            label = (
                address.get("city")
                or address.get("town")
                or address.get("village")
                or address.get("state")
                or data.get("display_name")
            )
    label = label or f"{lat:.4f}, {lng:.4f}"
    geocode_cache[key] = label
    return label


async def autocomplete(query: str, lat: float | None = None, lng: float | None = None, limit: int = 8) -> list[dict]:
    settings = get_settings()
    if settings.google_enabled:
        return await _autocomplete_google(query, settings.google_maps_api_key, lat, lng, limit)
    return await _autocomplete_nominatim(query, limit)


async def wikipedia_image(name: str) -> tuple[str | None, str | None]:
    key = _cache_key("wiki", name.lower())
    if key in wiki_cache:
        return wiki_cache[key]
    try:
        async with httpx.AsyncClient(timeout=8, headers={"User-Agent": USER_AGENT}) as client:
            response = await client.get(
                f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(name)}",
            )
            if response.status_code != 200:
                wiki_cache[key] = (None, None)
                return None, None
            data = response.json()
            thumb = (data.get("thumbnail") or {}).get("source")
            extract = data.get("extract")
            result = (thumb, extract)
            wiki_cache[key] = result
            return result
    except httpx.HTTPError:
        wiki_cache[key] = (None, None)
        return None, None


async def _geocode_google(query: str, api_key: str) -> GeoPoint | None:
    async with httpx.AsyncClient(timeout=12) as client:
        response = await client.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={"address": query, "key": api_key},
        )
        data = response.json()
        results = data.get("results") or []
        if not results:
            return None
        loc = results[0]["geometry"]["location"]
        return GeoPoint(lat=loc["lat"], lng=loc["lng"], label=results[0].get("formatted_address", query))


async def _geocode_nominatim(query: str) -> GeoPoint | None:
    async with httpx.AsyncClient(timeout=12, headers={"User-Agent": USER_AGENT}) as client:
        response = await client.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": query, "format": "jsonv2", "limit": 1},
        )
        data = response.json()
        if not data:
            return None
        item = data[0]
        return GeoPoint(lat=float(item["lat"]), lng=float(item["lon"]), label=item.get("display_name", query))


async def _autocomplete_nominatim(query: str, limit: int) -> list[dict]:
    async with httpx.AsyncClient(timeout=10, headers={"User-Agent": USER_AGENT}) as client:
        response = await client.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": query,
                "format": "jsonv2",
                "limit": limit,
                "addressdetails": 1,
            },
        )
        data = response.json()
    results = []
    for item in data:
        address = item.get("address") or {}
        subtitle = ", ".join(
            part
            for part in [
                address.get("city") or address.get("town") or address.get("state"),
                address.get("country"),
            ]
            if part
        )
        results.append(
            {
                "id": str(item.get("place_id")),
                "label": item.get("name") or item.get("display_name", query).split(",")[0],
                "subtitle": subtitle or item.get("display_name"),
                "coords": {"lat": float(item["lat"]), "lng": float(item["lon"]), "label": item.get("display_name")},
            }
        )
    return results


async def _autocomplete_google(query: str, api_key: str, lat: float | None, lng: float | None, limit: int) -> list[dict]:
    params: dict = {"input": query, "key": api_key, "types": "geocode"}
    if lat is not None and lng is not None:
        params["location"] = f"{lat},{lng}"
        params["radius"] = 50000
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(
            "https://maps.googleapis.com/maps/api/place/autocomplete/json",
            params=params,
        )
        data = response.json()
    results = []
    for item in (data.get("predictions") or [])[:limit]:
        results.append(
            {
                "id": item.get("place_id"),
                "label": item.get("structured_formatting", {}).get("main_text") or item.get("description"),
                "subtitle": item.get("structured_formatting", {}).get("secondary_text"),
                "coords": None,
            }
        )
    return results
