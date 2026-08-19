import { useEffect } from "react";
import { MapContainer, Marker, Polyline, Popup, TileLayer, useMap } from "react-leaflet";
import L from "leaflet";
import type { DayPlan, GeoPoint, ItineraryStop } from "../types";

const DAY_COLORS = ["#cbb089", "#3e8f7c", "#8fb4d4", "#d4a09a", "#cbb089"];

function pinIcon(index: number, color: string) {
  return L.divIcon({
    className: "",
    html: `<div class="marker-pin" style="background:${color}"><span>${index}</span></div>`,
    iconSize: [28, 28],
    iconAnchor: [14, 28],
  });
}

function Fit({ points }: { points: [number, number][] }) {
  const map = useMap();
  useEffect(() => {
    if (points.length === 0) return;
    const bounds = L.latLngBounds(points);
    map.fitBounds(bounds.pad(0.18));
  }, [map, points]);
  return null;
}

export function TripMap({
  center,
  day,
  origin,
  selectedId,
  onSelect,
}: {
  center: GeoPoint;
  day: DayPlan;
  origin?: GeoPoint | null;
  selectedId?: string;
  onSelect: (stop: ItineraryStop) => void;
}) {
  const color = DAY_COLORS[(day.day - 1) % DAY_COLORS.length];
  const points: [number, number][] = day.stops.map((stop) => [stop.place.lat, stop.place.lng]);
  const start = origin ? ([origin.lat, origin.lng] as [number, number]) : null;
  const line = start ? [start, ...points] : points;

  return (
    <MapContainer
      key={`day-${day.day}`}
      center={[center.lat, center.lng]}
      zoom={12}
      scrollWheelZoom
      aria-label={`Map of day ${day.day}`}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
      />
      <Fit points={line} />
      {start && (
        <Marker position={start} icon={pinIcon(0, "#f4efe6")}>
          <Popup>Starting point</Popup>
        </Marker>
      )}
      {day.stops.map((stop, index) => (
        <Marker
          key={stop.id}
          position={[stop.place.lat, stop.place.lng]}
          icon={pinIcon(index + 1, selectedId === stop.id ? "#e0c49a" : color)}
          eventHandlers={{ click: () => onSelect(stop) }}
        >
          <Popup>
            <strong>{stop.place.name}</strong>
            <div>{stop.time} · {stop.place.category}</div>
          </Popup>
        </Marker>
      ))}
      {line.length > 1 && <Polyline positions={line} pathOptions={{ color, weight: 3, opacity: 0.85 }} />}
    </MapContainer>
  );
}
