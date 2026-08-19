import type { DayPlan, ItineraryStop } from "../types";

function formatTime(value: string) {
  const [h, m] = value.split(":").map(Number);
  const suffix = h >= 12 ? "PM" : "AM";
  const hour = ((h + 11) % 12) + 1;
  return `${hour}:${String(m).padStart(2, "0")} ${suffix}`;
}

export function ItineraryTimeline({
  day,
  selectedId,
  onSelect,
  onRemove,
}: {
  day: DayPlan;
  selectedId?: string;
  onSelect: (stop: ItineraryStop) => void;
  onRemove: (stop: ItineraryStop) => void;
}) {
  return (
    <div>
      <h2 style={{ fontSize: "2.1rem", marginBottom: 6 }}>
        Day {day.day} — {day.title}
      </h2>
      <p className="muted">{day.summary}</p>
      <div className="timeline" style={{ marginTop: 20 }}>
        {day.stops.map((stop) => (
          <article
            key={stop.id}
            className={`stop-card ${selectedId === stop.id ? "active-stop" : ""}`}
          >
            <button
              type="button"
              onClick={() => onSelect(stop)}
              style={{ all: "unset", cursor: "pointer", display: "block", width: "100%" }}
            >
              <div className="stop-time">{formatTime(stop.time)}</div>
              <h3 style={{ margin: "4px 0 0", fontSize: "1.35rem" }}>{stop.place.name}</h3>
              <div className="stop-meta">
                <span style={{ textTransform: "capitalize" }}>{stop.kind}</span>
                <span>{stop.duration_minutes} min</span>
                {stop.travel_from_previous_minutes > 0 && (
                  <span>
                    {stop.travel_from_previous_minutes} min travel · {stop.travel_from_previous_km.toFixed(1)} km
                  </span>
                )}
              </div>
              <p className="reason">{stop.explanation}</p>
            </button>
            <button className="btn btn-ghost btn-small" type="button" onClick={() => onRemove(stop)}>
              Remove
            </button>
          </article>
        ))}
      </div>
    </div>
  );
}
