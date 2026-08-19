from __future__ import annotations

from ..schemas.trip import BudgetCategory, BudgetEstimate, TripPreferences

REGION_MULTIPLIER = {
    "pakistan": 0.35,
    "india": 0.4,
    "nepal": 0.38,
    "thailand": 0.55,
    "indonesia": 0.5,
    "turkey": 0.7,
    "japan": 1.35,
    "switzerland": 1.7,
    "united states": 1.2,
    "uk": 1.25,
    "united kingdom": 1.25,
    "uae": 1.15,
    "dubai": 1.2,
}

BASE = {
    "budget": {
        "accommodation": (28, 55),
        "food": (18, 32),
        "transportation": (10, 22),
        "activities": (8, 20),
        "miscellaneous": (6, 14),
    },
    "moderate": {
        "accommodation": (70, 130),
        "food": (32, 60),
        "transportation": (18, 40),
        "activities": (18, 45),
        "miscellaneous": (12, 25),
    },
    "premium": {
        "accommodation": (180, 380),
        "food": (70, 140),
        "transportation": (40, 90),
        "activities": (45, 110),
        "miscellaneous": (30, 70),
    },
}

NOTES = {
    "accommodation": "Mid-range nightly stay near the itinerary cluster, scaled by trip length.",
    "food": "Daily meals based on your budget tier, not restaurant reservations.",
    "transportation": "Local driving, ride-hailing, and short transfers between stops.",
    "activities": "Tickets and experiences where attractions typically charge entry.",
    "miscellaneous": "Snacks, tips, and small incidentals.",
}


def estimate_budget(prefs: TripPreferences) -> BudgetEstimate:
    days = prefs.duration_days
    people = max(1, prefs.travelers_count if prefs.travelers != "solo" else 1)
    if prefs.travelers == "couple":
        people = max(people, 2)
    if prefs.travelers == "friends":
        people = max(people, 2)
    if prefs.travelers == "family":
        people = max(people, 3)

    multiplier = 1.0
    dest = prefs.destination.lower()
    for region, value in REGION_MULTIPLIER.items():
        if region in dest:
            multiplier = value
            break

    buckets = BASE[prefs.budget]
    categories = {}
    total_min = 0
    total_max = 0
    for key, (low, high) in buckets.items():
        scale = days * (people if key in {"food", "activities", "miscellaneous", "accommodation"} else max(1, people * 0.65))
        cat_min = int(low * scale * multiplier)
        cat_max = int(high * scale * multiplier)
        categories[key] = BudgetCategory(min=cat_min, max=cat_max, note=NOTES[key])
        total_min += cat_min
        total_max += cat_max

    return BudgetEstimate(
        currency="USD",
        is_estimate=True,
        disclaimer="These figures are planning estimates, not live prices or a booking quote.",
        accommodation=categories["accommodation"],
        food=categories["food"],
        transportation=categories["transportation"],
        activities=categories["activities"],
        miscellaneous=categories["miscellaneous"],
        total_min=total_min,
        total_max=total_max,
    )
