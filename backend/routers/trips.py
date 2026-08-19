from fastapi import APIRouter, HTTPException, Request

from ..limiter import limiter
from ..schemas.trip import ModifyTripRequest, ModifyTripResponse, PlanTripRequest, PlanTripResponse
from ..services.trip_planner import modify_trip, plan_trip
from ..utils.errors import AppError

router = APIRouter(prefix="/api/trips", tags=["trips"])


@router.post("/plan", response_model=PlanTripResponse)
@limiter.limit("8/minute")
async def plan_trip_endpoint(request: Request, body: PlanTripRequest) -> PlanTripResponse:
    if not body.natural_language and not body.destination:
        raise HTTPException(status_code=400, detail="Describe your trip or choose a destination.")
    try:
        return await plan_trip(body)
    except AppError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc


@router.post("/modify", response_model=ModifyTripResponse)
@limiter.limit("16/minute")
async def modify_trip_endpoint(request: Request, body: ModifyTripRequest) -> ModifyTripResponse:
    try:
        trip, message, changes = await modify_trip(
            body.trip, body.message, body.selected_day, body.selected_stop_id
        )
        return ModifyTripResponse(trip=trip, assistant_message=message, changes=changes)
    except AppError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
