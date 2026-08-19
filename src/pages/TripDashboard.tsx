import { useEffect, useMemo, useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { Assistant } from "../components/Assistant";
import { BudgetPanel } from "../components/BudgetPanel";
import { ItineraryTimeline } from "../components/ItineraryTimeline";
import { PlaceCard } from "../components/PlaceCard";
import { TripMap } from "../components/TripMap";
import { cacheDraft, getTrip, saveTrip } from "../storage";
import type { ItineraryStop, Trip } from "../types";

export function TripDashboard() {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const stateTrip = (location.state as { trip?: Trip; warnings?: string[] } | null)?.trip;
  const [trip, setTrip] = useState<Trip | null>(stateTrip || (id ? getTrip(id) : null) || null);
  const [dayIndex, setDayIndex] = useState(0);
  const [selected, setSelected] = useState<ItineraryStop | undefined>();
  const [showMap, setShowMap] = useState(true);
  const [saved, setSaved] = useState(false);
  const warnings = useMemo(() => {
    const fromState = (location.state as { warnings?: string[] } | null)?.warnings;
    if (fromState) return fromState;
    try {
      return JSON.parse(sessionStorage.getItem("ai-travel-guide.warnings") || "[]") as string[];
    } catch {
      return [];
    }
  }, [location.state]);

  useEffect(() => {
    if (trip) cacheDraft(trip);
  }, [trip]);

  const day = trip?.days[dayIndex];

  if (!trip || !day) {
    return (
      <main id="main" className="planner-page">
        <div className="panel empty">
          <h1>This trip is not on this device.</h1>
          <p>Generate a new itinerary or open one from My trips.</p>
          <button className="btn btn-primary" type="button" onClick={() => navigate("/plan")}>
            Plan a trip
          </button>
        </div>
      </main>
    );
  }

  return (
    <main id="main" className={`dashboard ${showMap ? "" : "map-hidden"}`}>
      <div className="dashboard-side">
        <div className="trip-head">
          <div className="eyebrow">{trip.preferences.destination}</div>
          <h1>{trip.title}</h1>
          <p className="muted">{trip.subtitle}</p>
          <div className="actions-row">
            <button
              className="btn btn-primary btn-small"
              type="button"
              onClick={() => {
                saveTrip(trip);
                setSaved(true);
              }}
            >
              {saved ? "Saved" : "Save trip"}
            </button>
            <button className="btn btn-ghost btn-small" type="button" onClick={() => navigate("/plan")}>
              Plan another
            </button>
          </div>
          {warnings.map((warning) => (
            <div className="warn" key={warning} style={{ marginBottom: 10 }}>
              {warning}
            </div>
          ))}
        </div>
        <div className="day-tabs" role="tablist" aria-label="Itinerary days">
          {trip.days.map((item, index) => (
            <button
              key={item.day}
              className={`day-tab ${index === dayIndex ? "active" : ""}`}
              type="button"
              onClick={() => {
                setDayIndex(index);
                setSelected(undefined);
              }}
            >
              Day {item.day}
            </button>
          ))}
        </div>
        <ItineraryTimeline
          day={day}
          selectedId={selected?.id}
          onSelect={setSelected}
          onRemove={async (stop) => {
            const next = {
              ...trip,
              days: trip.days.map((item) =>
                item.day === day.day
                  ? { ...item, stops: item.stops.filter((entry) => entry.id !== stop.id) }
                  : item
              ),
            };
            setTrip(next);
            cacheDraft(next);
          }}
        />
        <div className="card-grid" style={{ marginTop: 22, gridTemplateColumns: "1fr 1fr" }}>
          {trip.featured_places.slice(0, 4).map((place) => (
            <PlaceCard key={place.id} place={place} />
          ))}
        </div>
        <div style={{ height: 16 }} />
        <BudgetPanel budget={trip.budget} />
        <Assistant
          trip={trip}
          selectedDay={day.day}
          selectedStopId={selected?.id}
          onTrip={(next) => {
            setTrip(next);
            setSaved(false);
          }}
        />
        {trip.notes.length > 0 && (
          <p className="muted" style={{ marginTop: 16 }}>
            {trip.notes.join(" ")}
          </p>
        )}
      </div>
      <div className="map-wrap">
        <TripMap
          center={trip.map_center}
          day={day}
          origin={trip.preferences.origin_coords}
          selectedId={selected?.id}
          onSelect={setSelected}
        />
      </div>
      <button className="btn btn-primary mobile-map-toggle" type="button" onClick={() => setShowMap((value) => !value)}>
        {showMap ? "Show itinerary" : "Show map"}
      </button>
    </main>
  );
}
