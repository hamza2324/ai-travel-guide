from __future__ import annotations

import uuid
from datetime import datetime, timezone

from ..schemas.trip import GeoPoint, PlanTripRequest, PlanTripResponse, Trip, TripPreferences
from ..utils.errors import AppError, PlacesNotFoundError
from ..utils.geo import radius_for_trip
from . import ai_service
from .budget_service import estimate_budget
from .fallback_places import advisor_notes, blueprint_key
from .geocoding_service import geocode, reverse_geocode
from .itinerary_service import apply_less_driving, build_itinerary, featured_from_days, remove_stop, score_places
from .places_service import discover_places


async def plan_trip(request: PlanTripRequest) -> PlanTripResponse:
    pipeline = ["Understanding your travel style"]
    warnings: list[str] = []

    origin_label = request.origin
    if request.origin_coords and not origin_label:
        origin_label = await reverse_geocode(request.origin_coords.lat, request.origin_coords.lng)

    if request.natural_language:
        intent = await ai_service.extract_intent(request.natural_language, origin_label)
        pipeline.append("Extracting preferences from your request")
    else:
        intent = ai_service.heuristic_intent(request.destination or "", origin_label)

    try:
        prefs = ai_service.merge_preferences(intent, request.model_dump())
    except Exception as exc:
        raise AppError(str(exc) if "Please tell us" in str(exc) else "Tell us a destination to begin planning.", 400, "invalid_preferences") from exc

    if request.origin_coords:
        prefs.origin_coords = request.origin_coords
        prefs.origin = origin_label or prefs.origin

    dest_point = await geocode(prefs.destination)
    prefs.destination_coords = dest_point
    prefs.destination = dest_point.label.split(",")[0] if dest_point.label else prefs.destination

    start_point = dest_point
    if prefs.origin_coords:
        start_point = prefs.origin_coords
    elif prefs.origin:
        start_point = await geocode(prefs.origin)
        prefs.origin_coords = start_point

    pipeline.append("Discovering places you'll love")
    radius = radius_for_trip(prefs.duration_days, prefs.travel_style)
    places, source = await discover_places(
        dest_point.lat,
        dest_point.lng,
        prefs.interests,
        radius,
        prefs.travel_style,
        prefs.destination,
    )
    if len(places) < 4:
        raise PlacesNotFoundError()
    if len(places) < 10:
        warnings.append(
            "We found fewer places than expected for this area. The itinerary leans on the strongest matches."
        )

    pipeline.append("Scoring places against your interests")
    scored = score_places(places, prefs, dest_point.lat, dest_point.lng, radius)

    pipeline.append("Analyzing distances and grouping nearby stops")
    days = await build_itinerary(prefs, scored, (start_point.lat, start_point.lng))
    if not any(day.stops for day in days):
        raise PlacesNotFoundError()

    pipeline.append("Writing your personalized journey")
    featured = featured_from_days(days)
    narrative = await ai_service.generate_trip_narrative(
        prefs, featured, [day.theme for day in days]
    )
    has_guide_days = blueprint_key(prefs.destination) is not None
    titles = narrative.get("day_titles") or []
    summaries = narrative.get("day_summaries") or []
    for index, day in enumerate(days):
        if not has_guide_days and index < len(titles) and titles[index]:
            day.title = str(titles[index])[:56]
        if not has_guide_days and index < len(summaries) and summaries[index]:
            day.summary = str(summaries[index])[:240]

    trip = Trip(
        id=str(uuid.uuid4()),
        title=str(narrative.get("title") or f"{prefs.destination} · {prefs.duration_days} days"),
        subtitle=str(narrative.get("subtitle") or "A route-aware itinerary shaped around your interests."),
        preferences=prefs,
        days=days,
        featured_places=featured,
        budget=estimate_budget(prefs),
        map_center=GeoPoint(lat=dest_point.lat, lng=dest_point.lng, label=prefs.destination),
        created_at=datetime.now(timezone.utc).isoformat(),
        notes=advisor_notes(prefs.destination)
        + list(narrative.get("notes") or [])
        + [f"Places sourced from {source} and sequenced so each day covers a different corridor."],
    )
    pipeline.append("Ready")
    return PlanTripResponse(trip=trip, pipeline=pipeline, warnings=warnings)


async def modify_trip(trip: Trip, message: str, selected_day: int | None, selected_stop_id: str | None) -> tuple[Trip, str, list[str]]:
    parsed = await ai_service.interpret_modification(message, trip, selected_day, selected_stop_id)
    actions = parsed.get("actions") or []
    assistant_message = str(parsed.get("message") or "I've updated your itinerary.")
    changes: list[str] = []
    updated = trip

    for action in actions:
        action_type = (action.get("type") or "").lower()
        day_number = action.get("day") or selected_day
        stop_id = action.get("stop_id") or selected_stop_id

        if action_type == "remove":
            updated = remove_stop(updated, stop_id, day_number)
            changes.append("Removed a stop from the itinerary.")
        elif action_type == "less_driving":
            updated = apply_less_driving(updated)
            changes.append("Reduced driving by keeping fewer, closer stops.")
        elif action_type == "adjust_style" and action.get("travel_style") in {"relaxed", "balanced", "fast-paced"}:
            updated.preferences.travel_style = action["travel_style"]
            changes.append(f"Travel style set to {action['travel_style']}.")
        elif action_type == "adjust_budget" and action.get("budget") in {"budget", "moderate", "premium"}:
            updated.preferences.budget = action["budget"]
            from .budget_service import estimate_budget as refresh_budget

            updated.budget = refresh_budget(updated.preferences)
            changes.append(f"Budget tier updated to {action['budget']}.")
        elif action_type == "add_interest" and action.get("interest"):
            interest = action["interest"]
            if interest not in updated.preferences.interests:
                updated.preferences.interests.append(interest)
                changes.append(f"Added {interest} to your interests.")
        elif action_type in {"replace", "regenerate_day", "more_food"}:
            rebuilt = await _rebuild_affected_day(updated, day_number, action_type, action.get("query"))
            updated = rebuilt
            changes.append("Rebuilt the affected day using nearby alternatives.")

    if not changes:
        changes.append("No structural change was required.")
    return updated, assistant_message, changes


async def _rebuild_affected_day(trip: Trip, day_number: int | None, action_type: str, query: str | None) -> Trip:
    prefs: TripPreferences = trip.preferences
    dest = prefs.destination_coords or trip.map_center
    radius = radius_for_trip(prefs.duration_days, prefs.travel_style)
    places, _ = await discover_places(dest.lat, dest.lng, prefs.interests, radius, prefs.travel_style, prefs.destination)
    scored = score_places(places, prefs, dest.lat, dest.lng, radius)
    start = prefs.origin_coords or dest
    days = await build_itinerary(prefs, scored, (start.lat, start.lng))

    if day_number:
        replacement = next((day for day in days if day.day == day_number), None)
        if replacement:
            trip.days = [replacement if day.day == day_number else day for day in trip.days]
            trip.featured_places = featured_from_days(trip.days)
            return trip
    trip.days = days
    trip.featured_places = featured_from_days(days)
    return trip
