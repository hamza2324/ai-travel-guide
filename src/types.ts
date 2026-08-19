export type BudgetTier = "budget" | "moderate" | "premium";
export type TravelStyle = "relaxed" | "balanced" | "fast-paced";
export type TravelerType = "solo" | "friends" | "family" | "couple";

export const INTERESTS = [
  "mountains",
  "nature",
  "food",
  "photography",
  "history",
  "culture",
  "adventure",
  "shopping",
  "relaxation",
  "beaches",
  "wildlife",
  "nightlife",
] as const;

export type Interest = (typeof INTERESTS)[number];

export interface GeoPoint {
  lat: number;
  lng: number;
  label?: string | null;
}

export interface TripPreferences {
  destination: string;
  origin?: string | null;
  origin_coords?: GeoPoint | null;
  destination_coords?: GeoPoint | null;
  duration_days: number;
  start_date?: string | null;
  budget: BudgetTier;
  travelers: TravelerType;
  travelers_count: number;
  interests: string[];
  travel_style: TravelStyle;
  natural_language?: string | null;
}

export interface Place {
  id: string;
  name: string;
  category: string;
  lat: number;
  lng: number;
  rating?: number | null;
  user_ratings_total?: number | null;
  address?: string | null;
  photo_url?: string | null;
  opening_hours?: string[] | null;
  estimated_duration_minutes: number;
  tags: string[];
  match_score: number;
  price_level?: number | null;
  source: string;
  wikipedia_url?: string | null;
  description?: string | null;
  reasons: string[];
}

export interface ItineraryStop {
  id: string;
  day: number;
  time: string;
  end_time?: string | null;
  place: Place;
  kind: "attraction" | "meal" | "break" | "hotel" | "travel";
  duration_minutes: number;
  travel_from_previous_minutes: number;
  travel_from_previous_km: number;
  explanation: string;
  is_flexible: boolean;
}

export interface DayPlan {
  day: number;
  title: string;
  theme: string;
  summary: string;
  stops: ItineraryStop[];
  total_travel_minutes: number;
  total_attractions: number;
}

export interface BudgetCategory {
  min: number;
  max: number;
  note: string;
}

export interface BudgetEstimate {
  currency: string;
  is_estimate: boolean;
  disclaimer: string;
  accommodation: BudgetCategory;
  food: BudgetCategory;
  transportation: BudgetCategory;
  activities: BudgetCategory;
  miscellaneous: BudgetCategory;
  total_min: number;
  total_max: number;
}

export interface Trip {
  id: string;
  title: string;
  subtitle: string;
  preferences: TripPreferences;
  days: DayPlan[];
  featured_places: Place[];
  budget: BudgetEstimate;
  map_center: GeoPoint;
  created_at: string;
  notes: string[];
}

export interface PlanTripPayload {
  destination?: string;
  origin?: string;
  origin_coords?: GeoPoint;
  duration_days?: number;
  start_date?: string;
  budget?: BudgetTier;
  travelers?: TravelerType;
  travelers_count?: number;
  interests?: string[];
  travel_style?: TravelStyle;
  natural_language?: string;
}

export interface PlanTripResponse {
  trip: Trip;
  pipeline: string[];
  warnings: string[];
}

export interface PlaceSuggestion {
  id: string;
  label: string;
  subtitle?: string | null;
  coords?: GeoPoint | null;
}

export interface ModifyTripResponse {
  trip: Trip;
  assistant_message: string;
  changes: string[];
}
