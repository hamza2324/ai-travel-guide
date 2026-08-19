from __future__ import annotations

import json
import re
from typing import Any

import httpx

from ..config import get_settings
from ..schemas.ai import IntentPayload
from ..schemas.trip import ALLOWED_INTERESTS, Place, Trip, TripPreferences
from ..utils.errors import AIServiceError

JSON_BLOCK = re.compile(r"\{.*\}", re.DOTALL)


async def chat_json(system: str, user: str, temperature: float = 0.2) -> dict[str, Any]:
    raw = await chat_text(system, user, temperature=temperature)
    parsed = _extract_json(raw)
    if parsed is None:
        raise AIServiceError("The planner returned an unexpected response. Please try again.")
    return parsed


async def chat_text(system: str, user: str, temperature: float = 0.3) -> str:
    settings = get_settings()
    if not settings.ai_enabled:
        raise AIServiceError("Add an OPENROUTER_API_KEY to enable AI planning.")

    payload: dict[str, Any] = {
        "model": settings.openrouter_model,
        "temperature": temperature,
        "max_tokens": 1800,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    if settings.openrouter_provider:
        payload["provider"] = {"order": [settings.openrouter_provider], "allow_fallbacks": True}

    try:
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(
                f"{settings.openrouter_base_url.rstrip('/')}/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.openrouter_api_key}",
                    "HTTP-Referer": settings.app_referer,
                    "X-Title": settings.app_name,
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            if response.status_code >= 400:
                raise AIServiceError()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            return content.strip()
    except (httpx.HTTPError, KeyError, IndexError):
        raise AIServiceError()


def _extract_json(text: str) -> dict[str, Any] | None:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text).strip()
        text = re.sub(r"```$", "", text).strip()
    try:
        data = json.loads(text)
        return data if isinstance(data, dict) else None
    except json.JSONDecodeError:
        match = JSON_BLOCK.search(text)
        if not match:
            return None
        try:
            data = json.loads(match.group(0))
            return data if isinstance(data, dict) else None
        except json.JSONDecodeError:
            return None


async def extract_intent(text: str, origin: str | None = None) -> IntentPayload:
    system = (
        "You are the intent parser for AI Travel Guide, a premium trip planner. "
        "Extract structured travel preferences from the user's request. "
        "Return ONLY valid JSON with keys: destination, origin, duration_days, budget, "
        "travelers, travelers_count, interests, travel_style, start_date, confidence, follow_up, title_hint. "
        "Rules: budget must be one of budget|moderate|premium. "
        "travelers must be one of solo|friends|family|couple. "
        "travel_style must be one of relaxed|balanced|fast-paced. "
        f"interests must be a subset of {ALLOWED_INTERESTS}. "
        "duration_days is an integer 1-14. confidence is 0-1. "
        "If a field is unknown, use null. Do not invent a destination if none is stated."
    )
    user = f"User request:\n{text}\n"
    if origin:
        user += f"\nKnown starting location: {origin}"
    try:
        data = await chat_json(system, user, temperature=0.1)
        payload = IntentPayload.model_validate(data)
        if payload.interests:
            payload.interests = [i for i in payload.interests if i in ALLOWED_INTERESTS]
        return payload
    except (AIServiceError, ValueError):
        return heuristic_intent(text, origin)


def heuristic_intent(text: str, origin: str | None = None) -> IntentPayload:
    lowered = text.lower()
    duration = 3
    for days in range(14, 0, -1):
        if re.search(rf"\b{days}[ -]?day", lowered) or re.search(rf"\b{days} days\b", lowered):
            duration = days
            break
    if "weekend" in lowered:
        duration = 2
    if "one-day" in lowered or "one day" in lowered or "day trip" in lowered:
        duration = 1

    budget: str = "moderate"
    if any(word in lowered for word in ["budget", "cheap", "affordable", "backpack"]):
        budget = "budget"
    elif any(word in lowered for word in ["luxury", "premium", "splurge", "five star"]):
        budget = "premium"

    travelers = "solo"
    if any(word in lowered for word in ["friends", "mates", "group"]):
        travelers = "friends"
    elif any(word in lowered for word in ["family", "kids", "parents"]):
        travelers = "family"
    elif any(word in lowered for word in ["couple", "honeymoon", "romantic", "partner"]):
        travelers = "couple"

    style = "balanced"
    if any(word in lowered for word in ["relax", "slow", "chill", "minimal driving"]):
        style = "relaxed"
    elif any(word in lowered for word in ["packed", "fast", "adventure-packed", "as much as"]):
        style = "fast-paced"

    interests = [item for item in ALLOWED_INTERESTS if item in lowered]
    if "scenic" in lowered and "photography" not in interests:
        interests.append("photography")
    if "scenic" in lowered and "nature" not in interests:
        interests.append("nature")
    if not interests:
        interests = ["nature", "food"]

    destination = None
    to_match = re.search(r"\bto ([A-Z][A-Za-z\s]{2,40})", text)
    in_match = re.search(r"\bin ([A-Z][A-Za-z\s]{2,40})", text)
    if to_match:
        destination = to_match.group(1).split(".")[0].strip()
    elif in_match:
        destination = in_match.group(1).split(".")[0].strip()

    return IntentPayload(
        destination=destination,
        origin=origin,
        duration_days=duration,
        budget=budget,  # type: ignore[arg-type]
        travelers=travelers,  # type: ignore[arg-type]
        interests=interests,
        travel_style=style,  # type: ignore[arg-type]
        confidence=0.45,
        follow_up=None if destination else "Where would you like to go?",
    )


def merge_preferences(intent: IntentPayload, request_data: dict[str, Any]) -> TripPreferences:
    destination = request_data.get("destination") or intent.destination
    if not destination:
        destination = request_data.get("origin") or intent.origin
    if not destination:
        raise AIServiceError("Please tell us where you want to go so we can plan a real itinerary.")
    interests = request_data.get("interests") or intent.interests or ["nature"]
    return TripPreferences(
        destination=destination,
        origin=request_data.get("origin") or intent.origin,
        origin_coords=request_data.get("origin_coords"),
        duration_days=request_data.get("duration_days") or intent.duration_days or 3,
        start_date=request_data.get("start_date") or intent.start_date,
        budget=request_data.get("budget") or intent.budget or "moderate",
        travelers=request_data.get("travelers") or intent.travelers or "solo",
        travelers_count=request_data.get("travelers_count") or intent.travelers_count or 1,
        interests=interests,
        travel_style=request_data.get("travel_style") or intent.travel_style or "balanced",
        natural_language=request_data.get("natural_language"),
    )


async def generate_trip_narrative(prefs: TripPreferences, featured: list[Place], day_themes: list[str]) -> dict[str, Any]:
    system = (
        "You write concise, premium travel-planner copy. Return ONLY JSON with keys: "
        "title, subtitle, day_titles (array of short titles), day_summaries (array), notes (array of 2-4 practical notes). "
        "No hashtags. No emojis. Keep titles editorial, not clickbait."
    )
    names = ", ".join(place.name for place in featured[:8])
    user = (
        f"Destination: {prefs.destination}\n"
        f"Days: {prefs.duration_days}\n"
        f"Budget: {prefs.budget}\n"
        f"Travelers: {prefs.travelers}\n"
        f"Style: {prefs.travel_style}\n"
        f"Interests: {', '.join(prefs.interests)}\n"
        f"Suggested day themes: {', '.join(day_themes)}\n"
        f"Key places: {names}"
    )
    try:
        return await chat_json(system, user, temperature=0.4)
    except AIServiceError:
        return {
            "title": f"{prefs.destination} in {prefs.duration_days} days",
            "subtitle": "A route-aware itinerary shaped around your interests.",
            "day_titles": [f"Day {i + 1}" for i in range(prefs.duration_days)],
            "day_summaries": day_themes,
            "notes": [
                "Travel times are estimates and can change with traffic.",
                "Confirm opening hours locally before you go.",
            ],
        }


async def explain_stop(place: Place, previous: str | None, travel_minutes: int, interests: list[str]) -> str:
    reasons = place.reasons or []
    interest_text = ", ".join(interests[:3])
    if previous and travel_minutes:
        geo = f"It follows {previous} with about {travel_minutes} minutes of travel, keeping the day efficient."
    elif previous:
        geo = f"It sits close to {previous}, reducing unnecessary backtracking."
    else:
        geo = "It is a strong opening location for the day."
    match = reasons[0] if reasons else f"it aligns with {interest_text}"
    return f"Recommended because {match}, and {geo[0].lower() + geo[1:]}"


async def interpret_modification(message: str, trip: Trip, selected_day: int | None, selected_stop_id: str | None) -> dict[str, Any]:
    system = (
        "You interpret itinerary edit requests for AI Travel Guide. Return ONLY JSON: "
        '{"actions":[{"type":"remove|replace|regenerate_day|add_interest|adjust_style|adjust_budget|less_driving|more_food|reorder",'
        '"day":1,"stop_id":null,"interest":null,"travel_style":null,"budget":null,"query":null}],'
        '"message":"short confirmation"}. '
        "Use only the action types listed. If the user wants scenic instead of a museum, use replace with query. "
        "If they want less driving, use less_driving. Keep message under 40 words."
    )
    compact = {
        "destination": trip.preferences.destination,
        "style": trip.preferences.travel_style,
        "interests": trip.preferences.interests,
        "budget": trip.preferences.budget,
        "selected_day": selected_day,
        "selected_stop_id": selected_stop_id,
        "days": [
            {
                "day": day.day,
                "stops": [{"id": stop.id, "name": stop.place.name, "kind": stop.kind, "category": stop.place.category} for stop in day.stops],
            }
            for day in trip.days
        ],
    }
    user = f"Current trip:\n{json.dumps(compact)}\n\nUser request:\n{message}"
    try:
        return await chat_json(system, user, temperature=0.1)
    except AIServiceError:
        return heuristic_modification(message, selected_day, selected_stop_id)


def heuristic_modification(message: str, selected_day: int | None, selected_stop_id: str | None) -> dict[str, Any]:
    lowered = message.lower()
    actions: list[dict[str, Any]] = []
    if "less driving" in lowered or "minimal driving" in lowered or "too much travel" in lowered:
        actions.append({"type": "less_driving", "day": selected_day})
    if "more food" in lowered or "restaurant" in lowered or "cheaper restaurants" in lowered:
        actions.append({"type": "more_food", "day": selected_day, "query": "restaurant"})
    if "photography" in lowered:
        actions.append({"type": "add_interest", "interest": "photography"})
    if "relax" in lowered:
        actions.append({"type": "adjust_style", "travel_style": "relaxed"})
    if "replace" in lowered or "instead" in lowered or "scenic" in lowered:
        actions.append({"type": "replace", "day": selected_day, "stop_id": selected_stop_id, "query": "viewpoint"})
    if "remove" in lowered or "drop" in lowered or "skip" in lowered:
        actions.append({"type": "remove", "day": selected_day, "stop_id": selected_stop_id})
    if "regenerate" in lowered or "redo this day" in lowered:
        actions.append({"type": "regenerate_day", "day": selected_day})
    if not actions:
        actions.append({"type": "regenerate_day", "day": selected_day})
    return {
        "actions": actions,
        "message": "I've updated the itinerary based on your request.",
    }
