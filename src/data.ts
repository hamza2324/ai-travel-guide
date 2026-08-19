export const IMAGES = {
  hero: "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=2200&q=80",
  split: "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1600&q=80",
  moods: {
    adventure: "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5?auto=format&fit=crop&w=800&q=80",
    nature: "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=800&q=80",
    photography: "https://images.unsplash.com/photo-1491555103944-7c647fd097b8?auto=format&fit=crop&w=800&q=80",
    food: "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=80",
    history: "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=800&q=80",
    relaxation: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
  },
  categories: {
    viewpoint: "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=900&q=80",
    museum: "https://images.unsplash.com/photo-1572953109213-3be92343fc5c?auto=format&fit=crop&w=900&q=80",
    historic: "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=900&q=80",
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
  } as Record<string, string>,
};

export const MOODS = [
  { id: "adventure", label: "Adventure", interests: ["adventure", "mountains"], style: "fast-paced" as const, image: IMAGES.moods.adventure },
  { id: "nature", label: "Nature Escape", interests: ["nature", "mountains"], style: "relaxed" as const, image: IMAGES.moods.nature },
  { id: "photography", label: "Photography", interests: ["photography", "nature"], style: "balanced" as const, image: IMAGES.moods.photography },
  { id: "food", label: "Food Journey", interests: ["food", "culture"], style: "relaxed" as const, image: IMAGES.moods.food },
  { id: "history", label: "History", interests: ["history", "culture"], style: "balanced" as const, image: IMAGES.moods.history },
  { id: "relaxation", label: "Relaxation", interests: ["relaxation", "nature"], style: "relaxed" as const, image: IMAGES.moods.relaxation },
];

export function categoryImage(category: string, fallback?: string | null) {
  if (fallback) return fallback;
  return IMAGES.categories[category] || IMAGES.categories.attraction;
}

export const ATTRIBUTION =
  "Hero and mood photography via Unsplash. Map data © OpenStreetMap contributors. Routing via OSRM.";
