from ..schemas.trip import Place

def _p(
    pid: str,
    name: str,
    category: str,
    lat: float,
    lng: float,
    rating: float,
    tags: list[str],
    duration: int = 70,
) -> Place:
    return Place(
        id=pid,
        name=name,
        category=category,
        lat=lat,
        lng=lng,
        rating=rating,
        user_ratings_total=420,
        estimated_duration_minutes=duration,
        tags=tags,
        source="curated",
        address=name,
    )


ISLAMABAD = [
    _p("c-faisal", "Faisal Mosque", "religious", 33.7295, 73.0379, 4.8, ["architecture", "photography", "culture"], 75),
    _p("c-daman", "Daman-e-Koh", "viewpoint", 33.7394, 73.0551, 4.6, ["viewpoint", "photography", "mountains"], 55),
    _p("c-monument", "Pakistan Monument", "historic", 33.6931, 73.0686, 4.6, ["historic", "photography"], 70),
    _p("c-lok", "Lok Virsa Museum", "museum", 33.6908, 73.0675, 4.5, ["culture", "history"], 100),
    _p("c-trail", "Trail 5, Margalla Hills", "nature", 33.749, 73.064, 4.7, ["mountains", "adventure", "nature"], 110),
    _p("c-saidpur", "Saidpur Village", "historic", 33.7417, 73.066, 4.4, ["food", "culture"], 80),
    _p("c-centaurus", "The Centaurus Mall", "shopping", 33.7078, 73.0498, 4.3, ["shopping"], 70),
    _p("c-rawal", "Rawal Lake View Park", "park", 33.698, 73.126, 4.4, ["nature", "relaxation"], 80),
    _p("c-shakar", "Shakarparian", "park", 33.6904, 73.0789, 4.4, ["nature", "photography"], 60),
    _p("c-monal", "The Monal", "restaurant", 33.7486, 73.0536, 4.4, ["food", "viewpoint"], 80),
    _p("c-savor", "Savor Foods", "restaurant", 33.6938, 73.0555, 4.3, ["food"], 60),
    _p("c-coffee", "Islamabad Club Cafe stretch", "cafe", 33.701, 73.035, 4.2, ["food", "relaxation"], 40),
    _p("c-bar", "Blue Area evening strip", "nightlife", 33.7105, 73.055, 4.1, ["nightlife"], 80),
    _p("c-hotel", "Serena Islamabad area", "hotel", 33.715, 73.098, 4.6, ["hotel"], 0),
]

ABBOTTABAD = [
    _p("a-ilyasi", "Ilyasi Masjid", "religious", 34.168, 73.264, 4.6, ["historic", "culture"], 45),
    _p("a-shimla", "Shimla Hill", "viewpoint", 34.199, 73.242, 4.5, ["mountains", "photography"], 60),
    _p("a-thandyani", "Thandiani", "viewpoint", 34.233, 73.367, 4.7, ["mountains", "nature"], 90),
    _p("a-harnoi", "Harnoi Lake", "nature", 34.123, 73.268, 4.4, ["nature", "relaxation"], 70),
    _p("a-sarban", "Sarban Hills", "nature", 34.155, 73.21, 4.5, ["adventure", "mountains"], 90),
    _p("a-food", "Abbottabad Food Street", "restaurant", 34.148, 73.221, 4.3, ["food"], 70),
    _p("a-cafe", "Pine Park cafe area", "cafe", 34.17, 73.24, 4.2, ["relaxation"], 40),
]

HUNZA = [
    _p("h-baltit", "Baltit Fort", "historic", 36.3254, 74.669, 4.8, ["history", "photography"], 90),
    _p("h-altit", "Altit Fort", "historic", 36.318, 74.678, 4.7, ["history", "culture"], 75),
    _p("h-eagle", "Eagle's Nest viewpoint", "viewpoint", 36.316, 74.65, 4.9, ["photography", "mountains"], 50),
    _p("h-attabad", "Attabad Lake", "nature", 36.337, 74.867, 4.8, ["nature", "adventure"], 90),
    _p("h-passu", "Passu Cones viewpoint", "viewpoint", 36.468, 74.895, 4.9, ["mountains", "photography"], 55),
    _p("h-hopper", "Hopper Glacier view", "nature", 36.31, 74.79, 4.6, ["mountains", "adventure"], 80),
    _p("h-cafe", "Café de Hunza", "cafe", 36.3166, 74.665, 4.6, ["food"], 40),
    _p("h-food", "Karimabad rooftop dinner", "restaurant", 36.316, 74.67, 4.5, ["food"], 75),
]

MURREE = [
    _p("m-mall", "Mall Road Murree", "shopping", 33.907, 73.394, 4.3, ["shopping", "culture"], 70),
    _p("m-pindi", "Pindi Point", "viewpoint", 33.894, 73.39, 4.5, ["photography", "mountains"], 50),
    _p("m-kashmir", "Kashmir Point", "viewpoint", 33.917, 73.396, 4.5, ["mountains"], 45),
    _p("m-patriata", "Patriata (New Murree)", "adventure", 33.84, 73.45, 4.4, ["adventure"], 100),
    _p("m-food", "Mall Road restaurants", "restaurant", 33.908, 73.395, 4.2, ["food"], 70),
]

LAHORE = [
    _p("l-badshahi", "Badshahi Mosque", "religious", 31.588, 74.3106, 4.8, ["history", "architecture"], 70),
    _p("l-fort", "Lahore Fort", "historic", 31.5881, 74.3142, 4.7, ["history"], 100),
    _p("l-wazir", "Wazir Khan Mosque", "religious", 31.583, 74.323, 4.8, ["culture", "photography"], 50),
    _p("l-shahi", "Shahi Hammam / walled city", "historic", 31.584, 74.325, 4.6, ["history", "culture"], 80),
    _p("l-food", "Fort Road Food Street", "restaurant", 31.586, 74.309, 4.6, ["food"], 80),
    _p("l-bagh", "Shalimar Gardens", "park", 31.5859, 74.3825, 4.5, ["relaxation", "history"], 70),
    _p("l-museum", "Lahore Museum", "museum", 31.568, 74.308, 4.5, ["culture"], 90),
]


CATALOG: list[tuple[list[str], list[Place]]] = [
    (["islamabad", "rawalpindi", "margalla"], ISLAMABAD),
    (["abbottabad", "nandiar", "thandiani"], ABBOTTABAD),
    (["hunza", "karimabad", "gilgit", "passu"], HUNZA),
    (["murree", "patriata"], MURREE),
    (["lahore", "walled city"], LAHORE),
]


def curated_for(destination: str) -> list[Place]:
    key = destination.lower()
    for needles, places in CATALOG:
        if any(needle in key for needle in needles):
            return [place.model_copy(deep=True) for place in places]
    return []
