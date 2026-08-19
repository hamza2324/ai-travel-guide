from fastapi import APIRouter, HTTPException

from ..schemas.ai import AnalyzeRequest, AnalyzeResponse
from ..schemas.trip import TripPreferences
from ..services.ai_service import extract_intent, merge_preferences
from ..utils.errors import AppError

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.post("/analyze-request", response_model=AnalyzeResponse)
async def analyze_request(body: AnalyzeRequest) -> AnalyzeResponse:
    try:
        intent = await extract_intent(body.text, body.origin)
        prefs = merge_preferences(
            intent,
            {
                "origin": body.origin,
                "origin_coords": body.origin_coords,
                "destination": intent.destination or "Nearby",
            },
        )
        if not intent.destination:
            prefs = TripPreferences(
                destination="Nearby",
                origin=body.origin,
                duration_days=intent.duration_days or 1,
                budget=intent.budget or "moderate",
                travelers=intent.travelers or "solo",
                interests=intent.interests or ["nature"],
                travel_style=intent.travel_style or "balanced",
                natural_language=body.text,
            )
        return AnalyzeResponse(
            preferences=prefs,
            confidence=intent.confidence or 0.6,
            follow_up=intent.follow_up,
        )
    except AppError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
