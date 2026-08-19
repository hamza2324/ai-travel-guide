from __future__ import annotations

import hashlib

import httpx

from ..config import get_settings
from ..utils.cache import route_cache
from ..utils.geo import estimate_drive_minutes, haversine_km


def _key(*parts: str) -> str:
    return hashlib.sha256("|".join(parts).encode()).hexdigest()


async def travel_between(
    lat1: float, lng1: float, lat2: float, lng2: float
) -> tuple[float, int]:
    distance = round(haversine_km(lat1, lng1, lat2, lng2), 2)
    cache_key = _key("route", f"{lat1:.4f}", f"{lng1:.4f}", f"{lat2:.4f}", f"{lng2:.4f}")
    if cache_key in route_cache:
        return route_cache[cache_key]

    settings = get_settings()
    minutes = None
    if settings.google_enabled:
        minutes = await _google_duration(lat1, lng1, lat2, lng2, settings.google_maps_api_key)
    if minutes is None:
        minutes = await _osrm_duration(lat1, lng1, lat2, lng2)
    if minutes is None:
        minutes = estimate_drive_minutes(distance)

    result = (distance, int(minutes))
    route_cache[cache_key] = result
    return result


async def route_polyline(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    if len(points) < 2:
        return points
    coords = ";".join(f"{lng},{lat}" for lat, lng in points)
    try:
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.get(
                f"https://router.project-osrm.org/route/v1/driving/{coords}",
                params={"overview": "simplified", "geometries": "geojson"},
            )
            data = response.json()
            routes = data.get("routes") or []
            if not routes:
                return points
            geometry = routes[0].get("geometry", {}).get("coordinates") or []
            return [(latlng[1], latlng[0]) for latlng in geometry]
    except httpx.HTTPError:
        return points


async def _osrm_duration(lat1: float, lng1: float, lat2: float, lng2: float) -> int | None:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                f"https://router.project-osrm.org/route/v1/driving/{lng1},{lat1};{lng2},{lat2}",
                params={"overview": "false"},
            )
            data = response.json()
            routes = data.get("routes") or []
            if not routes:
                return None
            return max(1, int(routes[0]["duration"] / 60))
    except httpx.HTTPError:
        return None


async def _google_duration(lat1: float, lng1: float, lat2: float, lng2: float, api_key: str) -> int | None:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                "https://maps.googleapis.com/maps/api/distancematrix/json",
                params={
                    "origins": f"{lat1},{lng1}",
                    "destinations": f"{lat2},{lng2}",
                    "mode": "driving",
                    "key": api_key,
                },
            )
            data = response.json()
            rows = data.get("rows") or []
            if not rows:
                return None
            element = rows[0]["elements"][0]
            if element.get("status") != "OK":
                return None
            return max(1, int(element["duration"]["value"] / 60))
    except (httpx.HTTPError, KeyError, IndexError):
        return None
