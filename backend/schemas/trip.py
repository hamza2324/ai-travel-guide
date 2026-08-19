from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

BudgetTier = Literal["budget", "moderate", "premium"]
TravelStyle = Literal["relaxed", "balanced", "fast-paced"]
TravelerType = Literal["solo", "friends", "family", "couple"]

ALLOWED_INTERESTS = [
    "mountains",
    "nature",
    "food",
    "photography",
    "history",
    "culture",
    "adventure",
    "shopping",
    "relaxation",
    "beaches",
    "wildlife",
    "nightlife",
]


class GeoPoint(BaseModel):
    lat: float
    lng: float
    label: str | None = None


class TripPreferences(BaseModel):
    destination: str = Field(..., min_length=2, max_length=120)
    origin: str | None = None
    origin_coords: GeoPoint | None = None
    destination_coords: GeoPoint | None = None
    duration_days: int = Field(default=3, ge=1, le=14)
    start_date: str | None = None
    budget: BudgetTier = "moderate"
    travelers: TravelerType = "solo"
    travelers_count: int = Field(default=1, ge=1, le=20)
    interests: list[str] = Field(default_factory=lambda: ["nature"])
    travel_style: TravelStyle = "balanced"
    natural_language: str | None = Field(default=None, max_length=2000)

    @field_validator("interests")
    @classmethod
    def normalize_interests(cls, value: list[str]) -> list[str]:
        cleaned: list[str] = []
        for item in value:
            key = item.strip().lower()
            if key in ALLOWED_INTERESTS and key not in cleaned:
                cleaned.append(key)
        return cleaned or ["nature"]

    @field_validator("destination", "origin")
    @classmethod
    def strip_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return " ".join(value.split())


class PlanTripRequest(BaseModel):
    destination: str | None = None
    origin: str | None = None
    origin_coords: GeoPoint | None = None
    duration_days: int | None = Field(default=None, ge=1, le=14)
    start_date: str | None = None
    budget: BudgetTier | None = None
    travelers: TravelerType | None = None
    travelers_count: int | None = Field(default=None, ge=1, le=20)
    interests: list[str] | None = None
    travel_style: TravelStyle | None = None
    natural_language: str | None = Field(default=None, max_length=2000)

    @field_validator("natural_language")
    @classmethod
    def strip_prompt(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned = value.strip()
        return cleaned or None


class PlacePhoto(BaseModel):
    url: str
    attribution: str | None = None


class Place(BaseModel):
    id: str
    name: str
    category: str
    lat: float
    lng: float
    rating: float | None = None
    user_ratings_total: int | None = None
    address: str | None = None
    photo_url: str | None = None
    opening_hours: list[str] | None = None
    estimated_duration_minutes: int = 60
    tags: list[str] = Field(default_factory=list)
    match_score: float = 0
    price_level: int | None = None
    source: str = "osm"
    wikipedia_url: str | None = None
    description: str | None = None
    reasons: list[str] = Field(default_factory=list)


class ItineraryStop(BaseModel):
    id: str
    day: int
    time: str
    end_time: str | None = None
    place: Place
    kind: Literal["attraction", "meal", "break", "hotel", "travel"] = "attraction"
    duration_minutes: int
    travel_from_previous_minutes: int = 0
    travel_from_previous_km: float = 0
    explanation: str
    is_flexible: bool = False


class DayPlan(BaseModel):
    day: int
    title: str
    theme: str
    summary: str
    stops: list[ItineraryStop]
    total_travel_minutes: int = 0
    total_attractions: int = 0


class BudgetCategory(BaseModel):
    min: int
    max: int
    note: str


class BudgetEstimate(BaseModel):
    currency: str = "USD"
    is_estimate: bool = True
    disclaimer: str
    accommodation: BudgetCategory
    food: BudgetCategory
    transportation: BudgetCategory
    activities: BudgetCategory
    miscellaneous: BudgetCategory
    total_min: int
    total_max: int


class Trip(BaseModel):
    id: str
    title: str
    subtitle: str
    preferences: TripPreferences
    days: list[DayPlan]
    featured_places: list[Place]
    budget: BudgetEstimate
    map_center: GeoPoint
    created_at: str
    notes: list[str] = Field(default_factory=list)


class PlanTripResponse(BaseModel):
    trip: Trip
    pipeline: list[str]
    warnings: list[str] = Field(default_factory=list)


class ModifyTripRequest(BaseModel):
    trip: Trip
    message: str = Field(..., min_length=2, max_length=1500)
    selected_day: int | None = Field(default=None, ge=1, le=14)
    selected_stop_id: str | None = None


class ModifyTripResponse(BaseModel):
    trip: Trip
    assistant_message: str
    changes: list[str] = Field(default_factory=list)
