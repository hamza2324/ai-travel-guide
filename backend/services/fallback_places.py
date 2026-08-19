from ..schemas.trip import Place

U = "https://images.unsplash.com"


def _p(
    pid: str,
    name: str,
    category: str,
    lat: float,
    lng: float,
    rating: float,
    tags: list[str],
    duration: int = 70,
    photo: str | None = None,
    description: str = "",
    area: str = "",
) -> Place:
    extra = [area] if area else []
    return Place(
        id=pid,
        name=name,
        category=category,
        lat=lat,
        lng=lng,
        rating=rating,
        user_ratings_total=420,
        estimated_duration_minutes=duration,
        tags=list(dict.fromkeys([*tags, *extra])),
        source="curated",
        address=name,
        photo_url=photo,
        description=description or None,
    )


HUNZA = [
    _p("h-baltit", "Baltit Fort", "historic", 36.3254, 74.669, 4.8, ["history", "photography", "culture"], 90,
       f"{U}/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=80",
       "700-year-old seat of the Mirs, overlooking Karimabad terraces.", "karimabad"),
    _p("h-bazaar", "Karimabad Bazaar", "shopping", 36.3165, 74.6658, 4.5, ["culture", "shopping", "food"], 70,
       f"{U}/photo-1526772662000-3f88f10405ff?auto=format&fit=crop&w=1200&q=80",
       "Handmade rugs, gemstones, and apricot oil along the old polo ground lane.", "karimabad"),
    _p("h-duikar", "Duikar / Eagle's Nest viewpoint", "viewpoint", 36.316, 74.65, 4.9, ["photography", "mountains"], 55,
       f"{U}/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80",
       "Classic sunset over Ultar and Ladyfinger Peak — go 45 minutes before dusk.", "karimabad"),
    _p("h-altit", "Altit Fort", "historic", 36.318, 74.678, 4.7, ["history", "culture"], 75,
       f"{U}/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1200&q=80",
       "Older than Baltit; walk the wooden balconies above the original Hunza settlement.", "altit"),
    _p("h-garden", "Altit Royal Garden", "park", 36.3174, 74.6795, 4.6, ["relaxation", "culture", "nature"], 50,
       f"{U}/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1200&q=80",
       "Apricot shade and canal water — a slow hour after the fort.", "altit"),
    _p("h-sacred", "Sacred Rocks of Hunza (Haldeikish)", "historic", 36.304, 74.678, 4.4, ["history", "photography"], 45,
       f"{U}/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80",
       "Petroglyphs on the ancient Silk Road, just below Karimabad.", "altit"),
    _p("h-waterfalls", "Hassanabad / Hunza waterfalls", "nature", 36.305, 74.64, 4.5, ["nature", "adventure"], 70,
       f"{U}/photo-1432405972618-c60b0195a8a8?auto=format&fit=crop&w=1200&q=80",
       "Short walk to glacial melt cascades used by the local power project.", "karimabad"),
    _p("h-attabad", "Attabad Lake", "nature", 36.337, 74.867, 4.8, ["nature", "adventure", "photography"], 100,
       f"{U}/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=80",
       "Turquoise lake formed in 2010. Boat crossing beats sitting on the highway.", "attabad"),
    _p("h-tunnel", "Attabad tunnels viewpoint", "viewpoint", 36.348, 74.86, 4.5, ["photography", "mountains"], 30,
       f"{U}/photo-1483728642387-6c3bdd6c93e5?auto=format&fit=crop&w=1200&q=80",
       "Pause at the lake-edge lay-bys — the colour shift is the story.", "attabad"),
    _p("h-hussaini", "Hussaini Suspension Bridge viewpoint", "adventure", 36.423, 74.855, 4.6, ["adventure", "photography"], 40,
       f"{U}/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80",
       "Watch locals cross; walking it is optional and exposed. Photograph from the north bank.", "hussaini"),
    _p("h-passu", "Passu Cones viewpoint", "viewpoint", 36.468, 74.895, 4.9, ["mountains", "photography"], 55,
       f"{U}/photo-1483728642387-6c3bdd6c93e5?auto=format&fit=crop&w=1200&q=80",
       "The cathedral spires of Passu — best in late morning side-light.", "passu"),
    _p("h-glacier", "Passu Glacier viewpoint", "nature", 36.476, 74.882, 4.7, ["mountains", "adventure", "nature"], 80,
       f"{U}/photo-1519904981063-b0cf448d479e?auto=format&fit=crop&w=1200&q=80",
       "Short walk from Passu village toward the snout; dust and ice in the same frame.", "passu"),
    _p("h-borith", "Borith Lake", "nature", 36.455, 74.86, 4.6, ["nature", "relaxation", "photography"], 70,
       f"{U}/photo-1439066615861-d1af74d74000?auto=format&fit=crop&w=1200&q=80",
       "High meadow lake above Passu. Quiet picnic, migratory birds in season.", "passu"),
    _p("h-yunz", "Yunz Valley meadows", "nature", 36.47, 74.91, 4.5, ["nature", "adventure"], 90,
       f"{U}/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1200&q=80",
       "Jeep or hike behind Passu for open grassland and cone views.", "passu"),
    _p("h-hopper", "Hopper Glacier viewpoint", "nature", 36.31, 74.79, 4.6, ["mountains", "adventure"], 90,
       f"{U}/photo-1486870591958-9b9d0d1dda99?auto=format&fit=crop&w=1200&q=80",
       "Nagar side of the river. The icefall sits above terraced fields.", "nagar"),
    _p("h-hoper", "Hoper village walk", "culture", 36.312, 74.795, 4.5, ["culture", "photography"], 60,
       f"{U}/photo-1526772662000-3f88f10405ff?auto=format&fit=crop&w=1200&q=80",
       "Stone houses and potato terraces facing the glacier.", "nagar"),
    _p("h-rakaposhi", "Rakaposhi viewpoint, Minapin", "viewpoint", 36.176, 74.578, 4.8, ["mountains", "photography"], 70,
       f"{U}/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80",
       "The 7,788 m wall of Rakaposhi from the Nagar road — unmissable on a clear day.", "nagar"),
    _p("h-gulmit", "Gulmit village", "culture", 36.388, 74.863, 4.6, ["culture", "history", "photography"], 70,
       f"{U}/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=80",
       "Old Wakhi settlement, polo ground, and wood-carved houses.", "gulmit"),
    _p("h-ondra", "Ondra Fort, Gulmit", "historic", 36.392, 74.86, 4.5, ["history", "viewpoint"], 60,
       f"{U}/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1200&q=80",
       "Short climb above Gulmit for Attabad and Passu in one sweep.", "gulmit"),
    _p("h-kamaris", "Kamaris village", "nature", 36.33, 74.72, 4.4, ["nature", "relaxation"], 80,
       f"{U}/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1200&q=80",
       "High hamlet above Karimabad. Fewer visitors, wider Ultar views.", "gulmit"),
    _p("h-khunjerab", "Khunjerab Pass", "adventure", 36.85, 75.427, 4.7, ["adventure", "mountains", "photography"], 180,
       f"{U}/photo-1483728642387-6c3bdd6c93e5?auto=format&fit=crop&w=1200&q=80",
       "4,693 m border with China. Needs a clear morning, passport, and a hired jeep from Sost.", "khunjerab"),
    _p("h-sost", "Sost bazaar", "shopping", 36.68, 74.82, 4.2, ["shopping", "culture"], 40,
       f"{U}/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=1200&q=80",
       "Last Pakistani market before the pass — fuel, snacks, SIM, and permits chat.", "khunjerab"),
    _p("h-cafe", "Café de Hunza", "cafe", 36.3166, 74.665, 4.6, ["food", "relaxation"], 40,
       f"{U}/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1200&q=80",
       "Walnut cake and espresso in Karimabad — a local ritual.", "karimabad"),
    _p("h-hidden", "Hidden Paradise Cafe", "cafe", 36.3172, 74.667, 4.5, ["food"], 40,
       f"{U}/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1200&q=80",
       "Terrace coffee with Ultar in frame.", "karimabad"),
    _p("h-food", "Karimabad rooftop dinner", "restaurant", 36.316, 74.67, 4.5, ["food"], 75,
       f"{U}/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=1200&q=80",
       "Chapshuro, diram fiti, and apricot oil — eat at dusk.", "karimabad"),
    _p("h-passu-food", "Passu Peak restaurant", "restaurant", 36.455, 74.894, 4.3, ["food"], 60,
       f"{U}/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=1200&q=80",
       "Simple mountain cooking opposite the cones.", "passu"),
    _p("h-gulmit-food", "Gulmit inn kitchen", "restaurant", 36.389, 74.864, 4.4, ["food"], 60,
       f"{U}/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1200&q=80",
       "Home-style Wakhi bread and apricot soup.", "gulmit"),
    _p("h-lake-food", "Attabad lakeside lunch", "restaurant", 36.34, 74.87, 4.3, ["food"], 55,
       f"{U}/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=1200&q=80",
       "Trout and chai after a boat hour.", "attabad"),
]

ISLAMABAD = [
    _p("c-faisal", "Faisal Mosque", "religious", 33.7295, 73.0379, 4.8, ["architecture", "photography", "culture"], 75,
       f"{U}/photo-1548013146-72479768bada?auto=format&fit=crop&w=1200&q=80", "Monumental tent-roof mosque at the foot of the Margallas.", "f-7"),
    _p("c-daman", "Daman-e-Koh", "viewpoint", 33.7394, 73.0551, 4.6, ["viewpoint", "photography", "mountains"], 55,
       f"{U}/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1200&q=80", "City-and-hills overlook. Go for late afternoon haze.", "margalla"),
    _p("c-monument", "Pakistan Monument", "historic", 33.6931, 73.0686, 4.6, ["historic", "photography"], 70,
       f"{U}/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=1200&q=80", "Petal monument and museum beneath.", "shakarparian"),
    _p("c-lok", "Lok Virsa Museum", "museum", 33.6908, 73.0675, 4.5, ["culture", "history"], 100,
       f"{U}/photo-1572953109213-3be92343fc5c?auto=format&fit=crop&w=1200&q=80", "Craft, music, and regional rooms — the best indoor hour in the capital.", "shakarparian"),
    _p("c-trail", "Trail 5, Margalla Hills", "nature", 33.749, 73.064, 4.7, ["mountains", "adventure", "nature"], 110,
       f"{U}/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1200&q=80", "Forest climb to a ridge view. Start early, carry water.", "margalla"),
    _p("c-saidpur", "Saidpur Village", "historic", 33.7417, 73.066, 4.4, ["food", "culture"], 80,
       f"{U}/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1200&q=80", "Restored village lane for lunch after Daman-e-Koh.", "margalla"),
    _p("c-centaurus", "The Centaurus Mall", "shopping", 33.7078, 73.0498, 4.3, ["shopping"], 70,
       f"{U}/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=1200&q=80", "Air-conditioned pause, not a sightseeing highlight.", "blue-area"),
    _p("c-rawal", "Rawal Lake View Park", "park", 33.698, 73.126, 4.4, ["nature", "relaxation"], 80,
       f"{U}/photo-1439066615861-d1af74d74000?auto=format&fit=crop&w=1200&q=80", "Reservoir edge for a slower afternoon.", "rawal"),
    _p("c-shakar", "Shakarparian", "park", 33.6904, 73.0789, 4.4, ["nature", "photography"], 60,
       f"{U}/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1200&q=80", "Pine lawns next to the monument.", "shakarparian"),
    _p("c-monal", "The Monal", "restaurant", 33.7486, 73.0536, 4.4, ["food", "viewpoint"], 80,
       f"{U}/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=1200&q=80", "Hill restaurant; go for the terrace, not the rush.", "margalla"),
    _p("c-savor", "Savor Foods", "restaurant", 33.6938, 73.0555, 4.3, ["food"], 60,
       f"{U}/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1200&q=80", "Reliable desi thaal, local prices.", "f-sectors"),
    _p("c-coffee", "F-6 / F-7 cafe stretch", "cafe", 33.721, 73.055, 4.2, ["food", "relaxation"], 40,
       f"{U}/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1200&q=80", "Khana, Coffee, and bookshop circuit.", "f-sectors"),
    _p("c-bar", "Blue Area evening strip", "nightlife", 33.7105, 73.055, 4.1, ["nightlife"], 80,
       f"{U}/photo-1566737236500-c8ac43014a67?auto=format&fit=crop&w=1200&q=80", "City lights after the hills.", "blue-area"),
    _p("c-rose", "Rose and Jasmine Garden", "park", 33.708, 73.078, 4.3, ["relaxation", "nature"], 50,
       f"{U}/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1200&q=80", "Seasonal blooms, easy walking.", "shakarparian"),
    _p("c-pir", "Pir Sohawa ridge", "viewpoint", 33.823, 73.1, 4.6, ["mountains", "photography"], 80,
       f"{U}/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80", "Higher ridge than Daman-e-Koh; cooler air.", "margalla"),
]

ABBOTTABAD = [
    _p("a-ilyasi", "Ilyasi Masjid", "religious", 34.168, 73.264, 4.6, ["historic", "culture"], 45, None, "Spring-fed mosque in a limestone fold.", "nathia"),
    _p("a-shimla", "Shimla Hill", "viewpoint", 34.199, 73.242, 4.5, ["mountains", "photography"], 60, None, "Pine ridge above town.", "abbottabad"),
    _p("a-thandyani", "Thandiani", "viewpoint", 34.233, 73.367, 4.7, ["mountains", "nature"], 90, None, "Cooler spur with Himalayan views — half-day jeep.", "thandiani"),
    _p("a-harnoi", "Harnoi Lake", "nature", 34.123, 73.268, 4.4, ["nature", "relaxation"], 70, None, "Picnic water on the Mansehra road.", "harnoi"),
    _p("a-sarban", "Sarban Hills", "nature", 34.155, 73.21, 4.5, ["adventure", "mountains"], 90, None, "Ridgeline walk west of the cantonment.", "abbottabad"),
    _p("a-food", "Abbottabad Food Street", "restaurant", 34.148, 73.221, 4.3, ["food"], 70, None, "Chapli and saffron tea.", "abbottabad"),
    _p("a-cafe", "Pine Park cafe", "cafe", 34.17, 73.24, 4.2, ["relaxation"], 40, None, "Shade and cake after the hill.", "abbottabad"),
    _p("a-nathia", "Nathia Gali viewpoint", "viewpoint", 34.091, 73.39, 4.6, ["mountains", "nature"], 90, None, "Galiyat classic if you have a full day.", "nathia"),
]

MURREE = [
    _p("m-mall", "Mall Road Murree", "shopping", 33.907, 73.394, 4.3, ["shopping", "culture"], 70, None, "Colonial ridge promenade — go early to beat the jam.", "murree"),
    _p("m-pindi", "Pindi Point", "viewpoint", 33.894, 73.39, 4.5, ["photography", "mountains"], 50, None, "Chairlift views toward the plains.", "murree"),
    _p("m-kashmir", "Kashmir Point", "viewpoint", 33.917, 73.396, 4.5, ["mountains"], 45, None, "Named for the distant Pir Panjal on a clear day.", "murree"),
    _p("m-patriata", "Patriata (New Murree)", "adventure", 33.84, 73.45, 4.4, ["adventure"], 100, None, "Gondola and pine walks, less cramped than the Mall.", "patriata"),
    _p("m-food", "Mall Road restaurants", "restaurant", 33.908, 73.395, 4.2, ["food"], 70, None, "Corn, chestnuts, and hotel buffets.", "murree"),
    _p("m-bhurban", "Bhurban pine loop", "nature", 33.95, 73.45, 4.4, ["nature", "relaxation"], 80, None, "Quieter ridge hotels and forest roads.", "bhurban"),
]

LAHORE = [
    _p("l-badshahi", "Badshahi Mosque", "religious", 31.588, 74.3106, 4.8, ["history", "architecture"], 70,
       f"{U}/photo-1548013146-72479768bada?auto=format&fit=crop&w=1200&q=80", "Mughal courtyard at the edge of the walled city.", "walled-city"),
    _p("l-fort", "Lahore Fort", "historic", 31.5881, 74.3142, 4.7, ["history"], 100,
       f"{U}/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=1200&q=80", "Sheesh Mahal light and the Picture Wall.", "walled-city"),
    _p("l-wazir", "Wazir Khan Mosque", "religious", 31.583, 74.323, 4.8, ["culture", "photography"], 50, None, "Frescoed tiles — the most photogenic interior in the city.", "walled-city"),
    _p("l-shahi", "Delhi Gate & Shahi Hammam", "historic", 31.584, 74.325, 4.6, ["history", "culture"], 80, None, "Walled-city lane into restored baths.", "walled-city"),
    _p("l-food", "Fort Road Food Street", "restaurant", 31.586, 74.309, 4.6, ["food"], 80, None, "Rooftops facing the mosque lights.", "walled-city"),
    _p("l-bagh", "Shalimar Gardens", "park", 31.5859, 74.3825, 4.5, ["relaxation", "history"], 70, None, "Three terraces of Mughal waterworks.", "mughalpura"),
    _p("l-museum", "Lahore Museum", "museum", 31.568, 74.308, 4.5, ["culture"], 90, None, "Gandhara sculpture and the Fasting Buddha.", "mall-road"),
    _p("l-minar", "Minar-e-Pakistan", "historic", 31.5925, 74.3095, 4.4, ["historic", "photography"], 40, None, "Iqbal Park after the fort.", "walled-city"),
    _p("l-anarkali", "Anarkali Bazaar", "shopping", 31.571, 74.312, 4.3, ["shopping", "food"], 70, None, "Old market denser than the malls.", "mall-road"),
]

SKARDU = [
    _p("s-kharpocho", "Skardu Fort (Kharpocho)", "historic", 35.304, 75.633, 4.6, ["history", "viewpoint"], 70, None, "Rock fort above the Indus.", "skardu"),
    _p("s-satpara", "Satpara Lake", "nature", 35.226, 75.628, 4.7, ["nature", "photography"], 80, None, "Alpine reservoir south of town.", "skardu"),
    _p("s-upper", "Upper Kachura Lake", "nature", 35.428, 75.458, 4.8, ["nature", "relaxation"], 90, None, "Shangrila's lake — go for the water, not the crowds.", "kachura"),
    _p("s-lower", "Lower Kachura / Shangrila", "park", 35.424, 75.455, 4.5, ["relaxation"], 60, None, "Resort lawns and the wreck-hotel island.", "kachura"),
    _p("s-sarfaranga", "Sarfaranga cold desert", "adventure", 35.34, 75.57, 4.6, ["adventure", "photography"], 80, None, "Sand dunes at 2,200 m.", "skardu"),
    _p("s-shigar", "Shigar Fort", "historic", 35.423, 75.738, 4.7, ["history", "culture"], 80, None, "Restored Raja fort, now a hotel — visit the public rooms.", "shigar"),
    _p("s-khaplu", "Khaplu Palace", "historic", 35.14, 76.337, 4.7, ["history"], 90, None, "Full-day east to Ghanche if you have time.", "khaplu"),
    _p("s-food", "Skardu bazaar dinner", "restaurant", 35.297, 75.633, 4.3, ["food"], 60, None, "Mamtu, apricot oil, and salt tea.", "skardu"),
]

NARAN = [
    _p("n-lake", "Lake Saif-ul-Malook", "nature", 34.877, 73.693, 4.8, ["nature", "mountains", "photography"], 120, None, "Jeep from Naran; go at first light to beat the convoy.", "saiful"),
    _p("n-babu", "Babusar Pass viewpoint", "viewpoint", 35.145, 74.05, 4.6, ["mountains", "adventure"], 150, None, "Only in summer, weather window required.", "babusar"),
    _p("n-lalazar", "Lalazar plateau", "nature", 34.92, 73.65, 4.6, ["nature", "photography"], 90, None, "Flower meadows above Naran.", "naran"),
    _p("n-bazaar", "Naran bazaar", "shopping", 34.907, 73.648, 4.2, ["shopping", "food"], 40, None, "Trout stalls and hotel row.", "naran"),
    _p("n-kunhar", "Kunhar river walk", "nature", 34.91, 73.65, 4.4, ["nature", "relaxation"], 50, None, "Evening along the water.", "naran"),
    _p("n-food", "Naran trout dinner", "restaurant", 34.908, 73.649, 4.4, ["food"], 70, None, "Fresh river trout is the honest meal here.", "naran"),
]


CATALOG: list[tuple[list[str], list[Place]]] = [
    (["islamabad", "rawalpindi", "margalla"], ISLAMABAD),
    (["abbottabad", "nandiar", "thandiani", "nathia"], ABBOTTABAD),
    (["hunza", "karimabad", "gilgit", "passu", "gulmit", "nagar", "altit"], HUNZA),
    (["murree", "patriata", "bhurban"], MURREE),
    (["lahore", "walled city"], LAHORE),
    (["skardu", "shigar", "khaplu", "kachura"], SKARDU),
    (["naran", "kaghan", "saif", "babusar"], NARAN),
]

# Professional day corridors: unique place IDs, in visit order. Never reuse an ID across days.
BLUEPRINTS: dict[str, list[list[str]]] = {
    "hunza": [
        ["h-baltit", "h-bazaar", "h-duikar"],
        ["h-altit", "h-garden", "h-sacred"],
        ["h-attabad", "h-tunnel", "h-hussaini"],
        ["h-passu", "h-glacier", "h-borith"],
        ["h-hopper", "h-hoper", "h-rakaposhi"],
        ["h-gulmit", "h-ondra", "h-kamaris"],
        ["h-khunjerab", "h-sost", "h-waterfalls"],
    ],
    "islamabad": [
        ["c-faisal", "c-daman", "c-saidpur"],
        ["c-monument", "c-lok", "c-shakar"],
        ["c-trail", "c-pir", "c-rawal"],
        ["c-rose", "c-centaurus"],
    ],
    "lahore": [
        ["l-badshahi", "l-fort", "l-minar"],
        ["l-wazir", "l-shahi", "l-anarkali"],
        ["l-bagh", "l-museum"],
    ],
    "skardu": [
        ["s-kharpocho", "s-satpara"],
        ["s-upper", "s-lower"],
        ["s-sarfaranga", "s-shigar"],
        ["s-khaplu"],
    ],
    "naran": [
        ["n-lake", "n-bazaar"],
        ["n-lalazar", "n-kunhar"],
        ["n-babu"],
    ],
    "murree": [
        ["m-mall", "m-pindi", "m-kashmir"],
        ["m-patriata", "m-bhurban"],
    ],
    "abbottabad": [
        ["a-ilyasi", "a-shimla", "a-food"],
        ["a-thandyani", "a-harnoi"],
        ["a-nathia", "a-sarban"],
    ],
}

BLUEPRINT_KEYS = {
    "hunza": ["hunza", "karimabad", "passu", "gulmit", "gilgit", "nagar", "altit"],
    "islamabad": ["islamabad", "rawalpindi", "margalla"],
    "lahore": ["lahore"],
    "skardu": ["skardu", "shigar", "khaplu"],
    "naran": ["naran", "kaghan", "saif"],
    "murree": ["murree", "patriata"],
    "abbottabad": ["abbottabad", "thandiani", "nathia"],
}

DAY_TITLES = {
    "hunza": [
        "Karimabad & Baltit",
        "Altit village",
        "Attabad Lake",
        "Passu cones & glacier",
        "Nagar & Rakaposhi",
        "Gulmit high hamlets",
        "Khunjerab Pass",
    ],
    "islamabad": ["Faisal & the Margallas", "Monuments & craft", "Trails & Rawal", "Gardens & the city"],
    "lahore": ["Badshahi & the Fort", "Walled city lanes", "Gardens & museum"],
    "skardu": ["Fort & Satpara", "Kachura lakes", "Desert & Shigar", "Khaplu palace"],
    "naran": ["Saif-ul-Malook", "Lalazar meadows", "Babusar Pass"],
    "murree": ["Mall Road ridge", "Patriata & Bhurban"],
    "abbottabad": ["Town & Ilyasi", "Thandiani", "Galiyat"],
}


def curated_for(destination: str) -> list[Place]:
    key = destination.lower()
    for needles, places in CATALOG:
        if any(needle in key for needle in needles):
            return [place.model_copy(deep=True) for place in places]
    return []


def advisor_notes(destination: str) -> list[str]:
    key = blueprint_key(destination)
    notes = {
        "hunza": [
            "Guide note: each day is a different valley corridor — Karimabad, Altit, Attabad, Passu, Nagar, Gulmit, then Khunjerab — not the same forts repeated.",
            "Khunjerab is a long, cold, high day. Leave Sost at dawn, carry passports, and skip it in heavy snow.",
            "Budget is in PKR using Hunza guesthouse, 4x4, and meal rates — not dollar hotel racks.",
        ],
        "islamabad": [
            "Margalla trails start early; Faisal Mosque interiors follow prayer times.",
            "Budget is in PKR from Islamabad hotel and Careem-range costs.",
        ],
        "lahore": [
            "Walled-city forts and mosques are a morning block; Shalimar is a separate drive east.",
            "Budget is in PKR using Lahore old-city and Mall Road ranges.",
        ],
        "skardu": [
            "Satpara, Kachura, Shigar, and the cold desert are separate half-days — do not stack them as one loop.",
            "Jeep and hotel rates are PKR field estimates for Baltistan.",
        ],
        "naran": [
            "Saif-ul-Malook is a first-light jeep. Babusar is weather-gated and a full day of its own.",
        ],
        "murree": [
            "Mall Road is the ridge. Patriata and Bhurban are the quieter second day.",
        ],
        "abbottabad": [
            "Thandiani and Nathia Gali are different spurs — plan them on separate days.",
        ],
    }
    return notes.get(key or "", ["Times include driving between stops. Estimates are labelled as estimates."])


def blueprint_key(destination: str) -> str | None:
    key = destination.lower()
    for name, needles in BLUEPRINT_KEYS.items():
        if any(needle in key for needle in needles):
            return name
    return None
