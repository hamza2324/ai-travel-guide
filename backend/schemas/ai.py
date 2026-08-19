from pydantic import BaseModel, Field

from .trip import BudgetTier, TravelerType, TravelStyle, TripPreferences


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=3, max_length=2000)
    origin: str | None = None
    origin_coords: dict | None = None


class AnalyzeResponse(BaseModel):
    preferences: TripPreferences
    confidence: float = 0.7
    follow_up: str | None = None


class IntentPayload(BaseModel):
    destination: str | None = None
    origin: str | None = None
    duration_days: int | None = None
    budget: BudgetTier | None = None
    travelers: TravelerType | None = None
    travelers_count: int | None = None
    interests: list[str] | None = None
    travel_style: TravelStyle | None = None
    start_date: str | None = None
    confidence: float | None = None
    follow_up: str | None = None
    title_hint: str | None = None
