from pydantic import BaseModel, Field

from .trip import GeoPoint, Place


class PlaceSearchQuery(BaseModel):
    q: str = Field(..., min_length=2, max_length=120)
    lat: float | None = None
    lng: float | None = None
    limit: int = Field(default=8, ge=1, le=15)


class PlaceSuggestion(BaseModel):
    id: str
    label: str
    subtitle: str | None = None
    coords: GeoPoint | None = None


class PlaceSearchResponse(BaseModel):
    results: list[PlaceSuggestion]


class NearbyPlacesRequest(BaseModel):
    destination: str
    coords: GeoPoint | None = None
    interests: list[str] = Field(default_factory=list)
    radius_km: int = Field(default=30, ge=5, le=120)


class NearbyPlacesResponse(BaseModel):
    places: list[Place]
    source: str
