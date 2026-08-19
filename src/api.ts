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
  const controller = new AbortController();
  const timer = window.setTimeout(() => controller.abort(), 120000);
  try {
    const response = await fetch(path, {
      headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
      signal: controller.signal,
      ...init,
    });
    if (!response.ok) {
      throw new Error(await parseError(response));
    }
    return response.json() as Promise<T>;
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new Error("Planning is taking longer than expected. Check the API is running, then try again.");
    }
    if (error instanceof TypeError) {
      throw new Error("Can't reach the planner. Start the API with python run.py, then try again.");
    }
    throw error;
  } finally {
    window.clearTimeout(timer);
  }
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
