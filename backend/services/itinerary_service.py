from __future__ import annotations

import uuid
from copy import deepcopy

from ..schemas.trip import DayPlan, ItineraryStop, Place, Trip, TripPreferences
from ..utils.geo import haversine_km
from .maps_service import travel_between
from .recommendation_service import (
    ATTRACTION_CATEGORIES,
    MEAL_CATEGORIES,
    add_minutes,
    compute_match_score,
    day_window,
    duration_for,
)

from .fallback_places import DAY_TITLES, BLUEPRINTS, blueprint_key


def score_places(
    places: list[Place],
    prefs: TripPreferences,
    center_lat: float,
    center_lng: float,
    radius_km: float,
) -> list[Place]:
    scored: list[Place] = []
    for place in places:
        clone = place.model_copy(deep=True)
        clone.estimated_duration_minutes = duration_for(clone.category, prefs.travel_style)
        score, reasons = compute_match_score(
            clone,
            prefs.interests,
            prefs.budget,
            prefs.travel_style,
            center_lat,
            center_lng,
            radius_km,
        )
        clone.match_score = score
        clone.reasons = reasons
        scored.append(clone)
    scored.sort(key=lambda item: item.match_score, reverse=True)
    return scored


def _is_meal(place: Place) -> bool:
    return place.category in MEAL_CATEGORIES


def _is_attraction(place: Place) -> bool:
    return place.category in ATTRACTION_CATEGORIES or place.category not in MEAL_CATEGORIES | {"hotel"}


def _dedupe(places: list[Place]) -> list[Place]:
    seen: set[str] = set()
    unique: list[Place] = []
    for place in places:
        key = place.name.strip().lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(place)
    return unique


def cluster_for_days(attractions: list[Place], days: int, per_day: int, destination: str = "") -> list[list[Place]]:
    unique = _dedupe(attractions)
    if not unique:
        return [[] for _ in range(days)]

    by_id = {place.id: place for place in unique}
    key = blueprint_key(destination)
    if key and key in BLUEPRINTS:
        clusters: list[list[Place]] = []
        used: set[str] = set()
        for corridor in BLUEPRINTS[key][:days]:
            group = []
            for pid in corridor:
                place = by_id.get(pid)
                if place and place.id not in used:
                    group.append(place)
                    used.add(place.id)
            clusters.append(group)
        leftovers = [place for place in unique if place.id not in used]
        while len(clusters) < days:
            clusters.append([])
        for place in leftovers:
            target = min(range(len(clusters)), key=lambda i: (len(clusters[i]), i))
            if len(clusters[target]) < per_day + 1:
                clusters[target].append(place)
        return clusters[:days]

    per_day = max(2, per_day)
    seeds: list[Place] = []
    pool = unique[:]
    seeds.append(pool.pop(0))
    while pool and len(seeds) < min(days, len(unique)):
        nxt = max(
            pool,
            key=lambda place: min(haversine_km(place.lat, place.lng, seed.lat, seed.lng) for seed in seeds),
        )
        seeds.append(nxt)
        pool.remove(nxt)

    clusters = [[seed] for seed in seeds]
    while len(clusters) < days:
        clusters.append([])

    for place in pool:
        open_days = [i for i, group in enumerate(clusters) if len(group) < per_day]
        if not open_days:
            i = min(range(len(clusters)), key=lambda idx: len(clusters[idx]))
            clusters[i].append(place)
            continue
        def score(i: int) -> float:
            if not clusters[i]:
                return 0
            return min(haversine_km(place.lat, place.lng, item.lat, item.lng) for item in clusters[i])
        best = min(open_days, key=score)
        clusters[best].append(place)

    richest = max(clusters, key=len)
    for i, group in enumerate(clusters):
        if group or len(richest) < 2:
            continue
        farthest = max(
            richest[1:],
            key=lambda item: haversine_km(richest[0].lat, richest[0].lng, item.lat, item.lng),
        )
        richest.remove(farthest)
        clusters[i] = [farthest]
        richest = max(clusters, key=len)
    return clusters[:days]


async def order_route(start: tuple[float, float], places: list[Place]) -> list[Place]:
    if not places:
        return []
    unused = places[:]
    ordered: list[Place] = []
    current = start
    while unused:
        unused.sort(key=lambda place: haversine_km(current[0], current[1], place.lat, place.lng) - place.match_score / 40)
        nxt = unused.pop(0)
        ordered.append(nxt)
        current = (nxt.lat, nxt.lng)
    if len(ordered) >= 4:
        ordered = _two_opt(start, ordered)
    return ordered


def _path_length(start: tuple[float, float], places: list[Place]) -> float:
    total = 0.0
    current = start
    for place in places:
        total += haversine_km(current[0], current[1], place.lat, place.lng)
        current = (place.lat, place.lng)
    return total


def _two_opt(start: tuple[float, float], places: list[Place]) -> list[Place]:
    best = places[:]
    improved = True
    while improved:
        improved = False
        for i in range(len(best) - 1):
            for j in range(i + 2, len(best)):
                candidate = best[:i] + list(reversed(best[i:j])) + best[j:]
                if _path_length(start, candidate) + 0.4 < _path_length(start, best):
                    best = candidate
                    improved = True
    return best


def nearest_meal(meals: list[Place], lat: float, lng: float, used_ids: set[str]) -> Place | None:
    candidates = [meal for meal in meals if meal.id not in used_ids]
    if not candidates:
        candidates = meals
    if not candidates:
        return None
    candidates.sort(key=lambda meal: haversine_km(lat, lng, meal.lat, meal.lng) - meal.match_score / 50)
    return candidates[0]


def synthetic_meal(name: str, lat: float, lng: float, kind: str) -> Place:
    return Place(
        id=f"meal-{uuid.uuid4().hex[:8]}",
        name=name,
        category="restaurant" if kind != "coffee" else "cafe",
        lat=lat,
        lng=lng,
        rating=4.3,
        match_score=72,
        tags=["food"],
        estimated_duration_minutes=60 if kind != "coffee" else 35,
        reasons=["keeps the day comfortable without a long detour"],
        description="A nearby meal stop placed to match the day's route.",
    )


async def build_day(
    day_index: int,
    attractions: list[Place],
    meals: list[Place],
    start: tuple[float, float],
    prefs: TripPreferences,
    used_ids: set[str],
) -> DayPlan:
    start_clock, end_clock, attraction_target = day_window(prefs.travel_style)
    day_places = [place for place in attractions if place.id not in used_ids]
    ordered = await order_route(start, day_places)
    ordered = ordered[:attraction_target]

    stops: list[ItineraryStop] = []
    cursor = start_clock
    current = start
    lunch_added = False
    dinner_added = False
    previous_name = None
    total_travel = 0

    async def append_stop(place: Place, kind: str, label_time: str | None = None) -> None:
        nonlocal cursor, current, previous_name, total_travel
        dist, minutes = await travel_between(current[0], current[1], place.lat, place.lng)
        minutes = 0 if not stops else max(minutes, 4 if dist > 0.15 else 0)
        if minutes:
            cursor = add_minutes(cursor, minutes)
        time_value = label_time or cursor
        duration = place.estimated_duration_minutes or duration_for(place.category, prefs.travel_style)
        explanation = _explanation(place, previous_name, minutes, prefs.interests)
        stop = ItineraryStop(
            id=f"stop-{uuid.uuid4().hex[:10]}",
            day=day_index,
            time=time_value,
            end_time=add_minutes(time_value, duration),
            place=place,
            kind=kind,  # type: ignore[arg-type]
            duration_minutes=duration,
            travel_from_previous_minutes=minutes,
            travel_from_previous_km=dist,
            explanation=explanation,
        )
        stops.append(stop)
        cursor = add_minutes(time_value, duration)
        current = (place.lat, place.lng)
        previous_name = place.name
        total_travel += minutes
        used_ids.add(place.id)

    breakfast = nearest_meal(
        [meal for meal in meals if meal.category == "cafe"] or meals,
        current[0],
        current[1],
        used_ids,
    ) or synthetic_meal("Breakfast nearby", current[0], current[1], "coffee")
    await append_stop(breakfast, "meal")

    for place in ordered:
        hour = int(cursor.split(":")[0])
        if not lunch_added and hour >= 12:
            meal = nearest_meal(meals, current[0], current[1], used_ids) or synthetic_meal(
                "Lunch nearby", current[0], current[1], "lunch"
            )
            await append_stop(meal, "meal")
            lunch_added = True
        if int(cursor.split(":")[0]) >= int(end_clock.split(":")[0]):
            break
        await append_stop(place, "attraction")
        used_ids.add(place.id)

    if not lunch_added and ordered:
        meal = nearest_meal(meals, current[0], current[1], used_ids) or synthetic_meal(
            "Lunch nearby", current[0], current[1], "lunch"
        )
        await append_stop(meal, "meal")

    hour = int(cursor.split(":")[0])
    if hour < 19 and prefs.travel_style != "relaxed":
        if not dinner_added:
            meal = nearest_meal(meals, current[0], current[1], used_ids) or synthetic_meal(
                "Dinner nearby", current[0], current[1], "dinner"
            )
            if hour < 18:
                cursor = "18:30" if hour < 18 else cursor
            await append_stop(meal, "meal")
            dinner_added = True
    elif not dinner_added:
        meal = nearest_meal(meals, current[0], current[1], used_ids) or synthetic_meal(
            "An easy dinner nearby", current[0], current[1], "dinner"
        )
        await append_stop(meal, "meal")

    theme = _day_title(prefs.destination, day_index, stops)
    attraction_names = [stop.place.name for stop in stops if stop.kind == "attraction"]
    if attraction_names:
        summary = (
            f"A {prefs.travel_style} field day: {', '.join(attraction_names[:3])}. "
            "Times are a realistic driving-and-walking sequence, not a copy of yesterday."
        )
    else:
        summary = f"A slower recovery day in {prefs.destination} — rest, food, and short walks."
    return DayPlan(
        day=day_index,
        title=theme,
        theme=theme,
        summary=summary,
        stops=stops,
        total_travel_minutes=total_travel,
        total_attractions=len([stop for stop in stops if stop.kind == "attraction"]),
    )


def _explanation(place: Place, previous: str | None, minutes: int, interests: list[str]) -> str:
    match = (place.reasons[0] if place.reasons else f"it matches {interests[0] if interests else 'your trip'}")
    if previous and minutes:
        return (
            f"Recommended because {match}. It is scheduled after {previous} "
            f"({minutes} min away) to keep the route compact."
        )
    if previous:
        return f"Recommended because {match}, and it sits close to {previous}."
    return f"Recommended because {match}, and it is a strong start to the day."


def _day_title(destination: str, day_index: int, stops: list[ItineraryStop]) -> str:
    key = blueprint_key(destination)
    titles = DAY_TITLES.get(key or "", [])
    if day_index - 1 < len(titles):
        return titles[day_index - 1]
    areas = [tag for stop in stops for tag in stop.place.tags if stop.kind == "attraction"]
    if areas:
        return areas[0].replace("-", " ").title()
    names = [stop.place.name for stop in stops if stop.kind == "attraction"]
    return names[0] if names else f"Day {day_index}"


async def build_itinerary(
    prefs: TripPreferences,
    places: list[Place],
    start: tuple[float, float],
) -> list[DayPlan]:
    attractions = [place for place in places if _is_attraction(place) and place.category != "hotel"]
    meals = [place for place in places if _is_meal(place)]
    if not meals:
        meals = [synthetic_meal(f"Local {label}", start[0], start[1], label) for label in ("breakfast cafe", "lunch", "dinner")]

    _, _, attraction_target = day_window(prefs.travel_style)
    clusters = cluster_for_days(attractions, prefs.duration_days, attraction_target, prefs.destination)
    used: set[str] = set()
    days: list[DayPlan] = []
    current_start = start
    for index, cluster in enumerate(clusters, start=1):
        day = await build_day(index, cluster, meals, current_start, prefs, used)
        days.append(day)
        last_attraction = next((stop for stop in reversed(day.stops) if stop.kind == "attraction"), None)
        if last_attraction:
            current_start = (last_attraction.place.lat, last_attraction.place.lng)
        elif prefs.travel_style == "relaxed":
            current_start = start
    return days


def featured_from_days(days: list[DayPlan], limit: int = 8) -> list[Place]:
    featured: list[Place] = []
    seen: set[str] = set()
    for day in days:
        for stop in day.stops:
            if stop.kind != "attraction":
                continue
            if stop.place.id in seen:
                continue
            seen.add(stop.place.id)
            featured.append(stop.place)
            if len(featured) >= limit:
                return featured
    return featured


def apply_less_driving(trip: Trip) -> Trip:
    updated = deepcopy(trip)
    updated.preferences.travel_style = "relaxed" if updated.preferences.travel_style == "fast-paced" else updated.preferences.travel_style
    for day in updated.days:
        attractions = [stop for stop in day.stops if stop.kind == "attraction"]
        if len(attractions) > 3:
            drop_ids = {stop.id for stop in attractions[3:]}
            day.stops = [stop for stop in day.stops if stop.id not in drop_ids]
            day.total_attractions = len([stop for stop in day.stops if stop.kind == "attraction"])
    return updated


def remove_stop(trip: Trip, stop_id: str | None, day_number: int | None) -> Trip:
    updated = deepcopy(trip)
    for day in updated.days:
        if day_number and day.day != day_number:
            continue
        before = len(day.stops)
        day.stops = [stop for stop in day.stops if stop.id != stop_id and stop.place.id != stop_id]
        if len(day.stops) != before:
            day.total_attractions = len([stop for stop in day.stops if stop.kind == "attraction"])
            break
    return updated
