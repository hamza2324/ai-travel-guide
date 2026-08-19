import { MapPin, Star } from "lucide-react";
import { categoryImage } from "../data";
import type { Place } from "../types";

export function PlaceCard({ place }: { place: Place }) {
  return (
    <article className="place-card">
      <div className="media-frame">
        <img
          src={categoryImage(place.category, place.photo_url)}
          alt=""
          loading="lazy"
        />
        <div className="match-badge">
          <strong>{Math.round(place.match_score)}%</strong>
          <div>AI MATCH</div>
        </div>
      </div>
      <div className="place-body">
        <h3 style={{ margin: "0 0 4px", fontSize: "1.45rem" }}>{place.name}</h3>
        <div className="muted" style={{ textTransform: "capitalize" }}>
          {place.category.replace("-", " ")}
        </div>
        <div className="stop-meta">
          {place.rating ? (
            <span>
              <Star size={14} aria-hidden /> {place.rating.toFixed(1)}
            </span>
          ) : null}
          <span>
            <MapPin size={14} aria-hidden /> {place.estimated_duration_minutes} min visit
          </span>
        </div>
        {place.tags.length > 0 && (
          <p className="reason">Best for: {place.tags.slice(0, 3).join(" · ")}</p>
        )}
      </div>
    </article>
  );
}
