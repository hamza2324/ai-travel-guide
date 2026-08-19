from fastapi import APIRouter, HTTPException, Query

from ..schemas.places import PlaceSearchResponse, PlaceSuggestion
from ..schemas.trip import GeoPoint
from ..services.geocoding_service import autocomplete, geocode, reverse_geocode
from ..utils.errors import AppError

router = APIRouter(prefix="/api/places", tags=["places"])


@router.get("/search", response_model=PlaceSearchResponse)
async def search_places(
    q: str = Query(..., min_length=2, max_length=120),
    lat: float | None = None,
    lng: float | None = None,
) -> PlaceSearchResponse:
    try:
        results = await autocomplete(q, lat, lng)
        suggestions = [
            PlaceSuggestion(
                id=item["id"],
                label=item["label"],
                subtitle=item.get("subtitle"),
                coords=GeoPoint(**item["coords"]) if item.get("coords") else None,
            )
            for item in results
        ]
        return PlaceSearchResponse(results=suggestions)
    except AppError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc


@router.get("/geocode")
async def geocode_endpoint(q: str = Query(..., min_length=2, max_length=120)) -> GeoPoint:
    try:
        return await geocode(q)
    except AppError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc


@router.get("/reverse")
async def reverse_endpoint(lat: float, lng: float) -> dict:
    try:
        label = await reverse_geocode(lat, lng)
        return {"label": label, "lat": lat, "lng": lng}
    except AppError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
