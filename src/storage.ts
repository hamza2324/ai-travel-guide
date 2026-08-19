import type { Trip } from "./types";

const KEY = "ai-travel-guide.trips";

export function loadTrips(): Trip[] {
  try {
    const raw = localStorage.getItem(KEY);
    return raw ? (JSON.parse(raw) as Trip[]) : [];
  } catch {
    return [];
  }
}

export function saveTrip(trip: Trip) {
  const trips = loadTrips().filter((item) => item.id !== trip.id);
  trips.unshift(trip);
  localStorage.setItem(KEY, JSON.stringify(trips.slice(0, 24)));
}

export function getTrip(id: string): Trip | undefined {
  return loadTrips().find((trip) => trip.id === id);
}

export function deleteTrip(id: string) {
  localStorage.setItem(KEY, JSON.stringify(loadTrips().filter((trip) => trip.id !== id)));
}

export function cacheDraft(trip: Trip) {
  sessionStorage.setItem("ai-travel-guide.current", JSON.stringify(trip));
}

export function readDraft(): Trip | null {
  try {
    const raw = sessionStorage.getItem("ai-travel-guide.current");
    return raw ? (JSON.parse(raw) as Trip) : null;
  } catch {
    return null;
  }
}
