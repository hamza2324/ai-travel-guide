from fastapi import APIRouter, HTTPException

from ..schemas.trip import PlanTripRequest, PlanTripResponse
from ..services.trip_planner import plan_trip
from ..utils.errors import AppError

router = APIRouter(prefix="/api/itinerary", tags=["itinerary"])


@router.post("/generate", response_model=PlanTripResponse)
async def generate_itinerary(body: PlanTripRequest) -> PlanTripResponse:
    try:
        return await plan_trip(body)
    except AppError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
