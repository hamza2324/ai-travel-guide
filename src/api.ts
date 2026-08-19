import type {
  ModifyTripResponse,
  PlaceSuggestion,
  PlanTripPayload,
  PlanTripResponse,
  Trip,
  TripPreferences,
} from "./types";

async function parseError(response: Response): Promise<string> {
  try {
    const data = await response.json();
    if (typeof data.detail === "string") return data.detail;
    if (Array.isArray(data.detail)) return data.detail.map((item: { msg?: string }) => item.msg).join(" ");
  } catch {
    /* ignore */
  }
  if (response.status === 429) return "Too many planning requests. Please wait a moment and try again.";
  return "We couldn't complete that request. Please try again.";
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
    ...init,
  });
  if (!response.ok) {
    throw new Error(await parseError(response));
  }
  return response.json() as Promise<T>;
}

export const api = {
  health: () => request<{ ok: boolean; ai: boolean; google_maps: boolean }>("/api/health"),
  searchPlaces: (q: string) =>
    request<{ results: PlaceSuggestion[] }>(`/api/places/search?q=${encodeURIComponent(q)}`),
  analyze: (text: string, origin?: string) =>
    request<{ preferences: TripPreferences; confidence: number; follow_up?: string }>("/api/ai/analyze-request", {
      method: "POST",
      body: JSON.stringify({ text, origin }),
    }),
  plan: (payload: PlanTripPayload) =>
    request<PlanTripResponse>("/api/trips/plan", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  modify: (trip: Trip, message: string, selected_day?: number, selected_stop_id?: string) =>
    request<ModifyTripResponse>("/api/trips/modify", {
      method: "POST",
      body: JSON.stringify({ trip, message, selected_day, selected_stop_id }),
    }),
};
