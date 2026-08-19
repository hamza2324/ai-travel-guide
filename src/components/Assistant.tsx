import { useState } from "react";
import { api } from "../api";
import { cacheDraft, saveTrip } from "../storage";
import type { Trip } from "../types";

export function Assistant({
  trip,
  selectedDay,
  selectedStopId,
  onTrip,
}: {
  trip: Trip;
  selectedDay?: number;
  selectedStopId?: string;
  onTrip: (trip: Trip) => void;
}) {
  const [message, setMessage] = useState("");
  const [log, setLog] = useState<{ role: "user" | "assistant"; text: string }[]>([
    {
      role: "assistant",
      text: `I have your ${trip.preferences.duration_days}-day ${trip.preferences.destination} itinerary. Ask me to replace a stop, add photography spots, or reduce driving.`,
    },
  ]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function send() {
    const text = message.trim();
    if (!text) return;
    setBusy(true);
    setError("");
    setLog((current) => [...current, { role: "user", text }]);
    setMessage("");
    try {
      const result = await api.modify(trip, text, selectedDay, selectedStopId);
      onTrip(result.trip);
      cacheDraft(result.trip);
      saveTrip(result.trip);
      setLog((current) => [
        ...current,
        { role: "assistant", text: `${result.assistant_message} ${result.changes.join(" ")}` },
      ]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "The assistant is unavailable right now.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="assistant panel" aria-label="Trip assistant">
      <h2 style={{ fontSize: "1.8rem" }}>Trip assistant</h2>
      <p className="muted">Aware of this itinerary, the selected day, and your preferences.</p>
      <div className="assistant-log">
        {log.map((item, index) => (
          <div key={index} className={`bubble ${item.role}`}>
            {item.text}
          </div>
        ))}
      </div>
      {error && <div className="alert">{error}</div>}
      <div className="hero-search" style={{ maxWidth: "none", borderRadius: 18 }}>
        <input
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          placeholder="Find cheaper restaurants near Day 2…"
          onKeyDown={(event) => event.key === "Enter" && send()}
          aria-label="Message the trip assistant"
        />
        <button className="btn btn-primary" type="button" onClick={send} disabled={busy}>
          {busy ? "Updating…" : "Send"}
        </button>
      </div>
    </section>
  );
}
