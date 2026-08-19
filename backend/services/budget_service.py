from __future__ import annotations

from ..schemas.trip import BudgetCategory, BudgetEstimate, TripPreferences

USD_TO_PKR = 278

# Per-person, per-day field rates in PKR (guesthouse/hotel, meals, local transport, tickets, extras).
# Northern jeep days are higher because a 4x4 is the actual way the valley is travelled.
PKR_DAILY = {
    "northern": {
        "budget": {"accommodation": (3500, 7000), "food": (1500, 2800), "transportation": (2500, 5000), "activities": (800, 2500), "miscellaneous": (600, 1400)},
        "moderate": {"accommodation": (8000, 16000), "food": (2800, 5000), "transportation": (6000, 12000), "activities": (2000, 6000), "miscellaneous": (1200, 2500)},
        "premium": {"accommodation": (22000, 45000), "food": (5500, 10000), "transportation": (14000, 25000), "activities": (5000, 12000), "miscellaneous": (2500, 5000)},
    },
    "city_pk": {
        "budget": {"accommodation": (4500, 8500), "food": (1800, 3200), "transportation": (800, 2200), "activities": (400, 1500), "miscellaneous": (500, 1200)},
        "moderate": {"accommodation": (12000, 22000), "food": (3500, 6500), "transportation": (1800, 4000), "activities": (1500, 4000), "miscellaneous": (1200, 2500)},
        "premium": {"accommodation": (28000, 65000), "food": (7000, 14000), "transportation": (3500, 8000), "activities": (4000, 10000), "miscellaneous": (2500, 6000)},
    },
    "hill_pk": {
        "budget": {"accommodation": (4000, 8000), "food": (1600, 3000), "transportation": (1500, 3500), "activities": (800, 2500), "miscellaneous": (600, 1400)},
        "moderate": {"accommodation": (10000, 20000), "food": (3000, 5500), "transportation": (3000, 7000), "activities": (2000, 5000), "miscellaneous": (1200, 2500)},
        "premium": {"accommodation": (25000, 55000), "food": (6000, 12000), "transportation": (8000, 16000), "activities": (4000, 9000), "miscellaneous": (2000, 4500)},
    },
}

INTERNATIONAL_USD = {
    "budget": {"accommodation": (28, 55), "food": (18, 32), "transportation": (10, 22), "activities": (8, 20), "miscellaneous": (6, 14)},
    "moderate": {"accommodation": (70, 130), "food": (32, 60), "transportation": (18, 40), "activities": (18, 45), "miscellaneous": (12, 25)},
    "premium": {"accommodation": (180, 380), "food": (70, 140), "transportation": (40, 90), "activities": (45, 110), "miscellaneous": (30, 70)},
}

NOTES = {
    "accommodation": "Nightly stay for the group, using typical guesthouse / hotel racks for this region — not a live booking quote.",
    "food": "Three meals a day at local dhabas through hotel restaurants, scaled to your tier.",
    "transportation": "Jeeps, Careem, or fuel for the actual distances in this itinerary. Hunza and Skardu assume 4x4 days.",
    "activities": "Fort tickets, boat hours, chairlifts, and park fees where they usually apply.",
    "miscellaneous": "Water, SIM/data, tips, and small bazaar spends.",
}


def _region(destination: str) -> str:
    text = destination.lower()
    northern = ["hunza", "karimabad", "gilgit", "passu", "skardu", "shigar", "khaplu", "naran", "kaghan", "swat", "chitral", "fairy", "nagar", "gulmit"]
    hills = ["murree", "abbottabad", "nathia", "thandiani", "galiyat", "patriata"]
    cities = ["islamabad", "rawalpindi", "lahore", "karachi", "peshawar", "multan", "faisalabad", "quetta"]
    if any(name in text for name in northern):
        return "northern"
    if any(name in text for name in hills):
        return "hill_pk"
    if any(name in text for name in cities) or "pakistan" in text:
        return "city_pk"
    return "international"


def estimate_budget(prefs: TripPreferences) -> BudgetEstimate:
    days = prefs.duration_days
    people = max(1, prefs.travelers_count)
    if prefs.travelers == "couple":
        people = max(people, 2)
    if prefs.travelers == "friends":
        people = max(people, 2)
    if prefs.travelers == "family":
        people = max(people, 3)
    if prefs.travelers == "solo":
        people = 1

    region = _region(prefs.destination)
    categories = {}
    total_min = 0
    total_max = 0

    if region == "international":
        buckets = INTERNATIONAL_USD[prefs.budget]
        for key, (low, high) in buckets.items():
            heads = people if key != "transportation" else max(1, people * 0.7)
            cat_min = int(low * days * heads * USD_TO_PKR)
            cat_max = int(high * days * heads * USD_TO_PKR)
            categories[key] = BudgetCategory(min=_round_pkr(cat_min), max=_round_pkr(cat_max), note=NOTES[key])
            total_min += categories[key].min
            total_max += categories[key].max
        where = "Converted to PKR from typical international daily rates."
    else:
        buckets = PKR_DAILY[region][prefs.budget]
        jeep_days = days if region == "northern" and days >= 2 else max(1, days - 1)
        for key, (low, high) in buckets.items():
            if key == "accommodation":
                cat_min, cat_max = low * days * max(1, (people + 1) // 2), high * days * max(1, (people + 1) // 2)
            elif key == "transportation" and region == "northern":
                # One jeep is shared; do not multiply blindly by every traveller.
                cat_min, cat_max = low * jeep_days, high * jeep_days
                if people > 4:
                    cat_min *= 2
                    cat_max *= 2
            else:
                cat_min, cat_max = low * days * people, high * days * people
            categories[key] = BudgetCategory(min=_round_pkr(int(cat_min)), max=_round_pkr(int(cat_max)), note=NOTES[key])
            total_min += categories[key].min
            total_max += categories[key].max
        label = {"northern": "Gilgit-Baltistan / northern valleys", "hill_pk": "Galiyat / hill stations", "city_pk": "Pakistani cities"}[region]
        where = f"Quoted in PKR from typical {label} field rates for a {prefs.budget} {prefs.travelers} trip."

    return BudgetEstimate(
        currency="PKR",
        is_estimate=True,
        disclaimer=(
            f"{where} These are planning ranges, not invoices. Jeep hire, peak-season hotels, "
            "and Khunjerab days move the top of the range."
        ),
        accommodation=categories["accommodation"],
        food=categories["food"],
        transportation=categories["transportation"],
        activities=categories["activities"],
        miscellaneous=categories["miscellaneous"],
        total_min=total_min,
        total_max=total_max,
    )


def _round_pkr(value: int) -> int:
    if value < 5000:
        return int(round(value / 100.0) * 100)
    return int(round(value / 500.0) * 500)
