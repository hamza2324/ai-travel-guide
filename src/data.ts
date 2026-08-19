export const IMAGES = {
  hero: "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=2400&q=80",
  heroAlt: "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5?auto=format&fit=crop&w=2400&q=80",
  split: "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1600&q=80",
  journal: "https://images.unsplash.com/photo-1519904981063-b0cf448d479e?auto=format&fit=crop&w=1400&q=80",
  lakes: "https://images.unsplash.com/photo-1439066615861-d1af74d74000?auto=format&fit=crop&w=1400&q=80",
  city: "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=1400&q=80",
  table: "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=1400&q=80",
  road: "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1400&q=80",
  video:
    "https://videos.pexels.com/video-files/3571264/3571264-hd_1920_1080_30fps.mp4",
  moods: {
    adventure: "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5?auto=format&fit=crop&w=900&q=80",
    nature: "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=900&q=80",
    photography: "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=900&q=80",
    food: "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=900&q=80",
    history: "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=900&q=80",
    relaxation: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=80",
  },
  categories: {
    viewpoint: "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=900&q=80",
    museum: "https://images.unsplash.com/photo-1572953109213-3be92343fc5c?auto=format&fit=crop&w=900&q=80",
    historic: "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=900&q=80",
    religious: "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=900&q=80",
    park: "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=900&q=80",
    nature: "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=900&q=80",
    restaurant: "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=900&q=80",
    cafe: "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=900&q=80",
    shopping: "https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=900&q=80",
    attraction: "https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?auto=format&fit=crop&w=900&q=80",
    hotel: "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=900&q=80",
    beach: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=80",
    nightlife: "https://images.unsplash.com/photo-1566737236500-c8ac43014a67?auto=format&fit=crop&w=900&q=80",
    adventure: "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5?auto=format&fit=crop&w=900&q=80",
  } as Record<string, string>,
};

export const FILMSTRIP = [
  IMAGES.hero,
  IMAGES.heroAlt,
  IMAGES.split,
  IMAGES.journal,
  IMAGES.lakes,
  IMAGES.city,
  IMAGES.table,
  IMAGES.road,
];

export const DESTINATIONS = [
  {
    name: "Hunza",
    line: "7 days · valleys & passes",
    query: "Plan a 7-day adventure trip to Hunza for two friends. We love mountains, photography, and food.",
    image: IMAGES.hero,
  },
  {
    name: "Islamabad",
    line: "3 days · trails & tables",
    query: "Plan a 3-day budget-friendly trip to Islamabad for two friends. We love mountains, food, photography, and historical places.",
    image: IMAGES.road,
  },
  {
    name: "Skardu",
    line: "5 days · lakes & light",
    query: "Plan a 5-day photography trip to Skardu with mountains, lakes, and a balanced pace.",
    image: IMAGES.lakes,
  },
  {
    name: "Lahore",
    line: "Weekend · food & forts",
    query: "Plan a 2-day food and history trip to Lahore for friends, moderate budget.",
    image: IMAGES.city,
  },
];

export const MOODS = [
  { id: "adventure", label: "Adventure", interests: ["adventure", "mountains"], style: "fast-paced" as const, image: IMAGES.moods.adventure },
  { id: "nature", label: "Nature Escape", interests: ["nature", "mountains"], style: "relaxed" as const, image: IMAGES.moods.nature },
  { id: "photography", label: "Photography", interests: ["photography", "nature"], style: "balanced" as const, image: IMAGES.moods.photography },
  { id: "food", label: "Food Journey", interests: ["food", "culture"], style: "relaxed" as const, image: IMAGES.moods.food },
  { id: "history", label: "History", interests: ["history", "culture"], style: "balanced" as const, image: IMAGES.moods.history },
  { id: "relaxation", label: "Relaxation", interests: ["relaxation", "nature"], style: "relaxed" as const, image: IMAGES.moods.relaxation },
];

export const FIELD_NOTES = [
  { title: "Move with the valley", body: "A Hunza week is seven corridors, not one fort seven times. Karimabad, Altit, Attabad, Passu, Nagar, Gulmit, Khunjerab." },
  { title: "Jeep is the plan", body: "Northern days are timed around 4x4 hours, altitude, and light — not a city walking tour pasted onto mountains." },
  { title: "Quoted in rupees", body: "Budgets use Pakistani guesthouse, meal, and jeep ranges so the number means something on the ground." },
];

export function categoryImage(category: string, fallback?: string | null) {
  if (fallback) return fallback;
  return IMAGES.categories[category] || IMAGES.categories.attraction;
}

export const ATTRIBUTION =
  "Cinematic stills via Unsplash. Hero motion via Pexels. Map data © OpenStreetMap contributors. Routing via OSRM. PKR ranges are field estimates, not invoices.";
