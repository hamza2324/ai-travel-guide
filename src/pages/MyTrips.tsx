import { useMemo } from "react";
import { Link, useNavigate } from "react-router-dom";
import { deleteTrip, loadTrips } from "../storage";
import { categoryImage, IMAGES } from "../data";

export function MyTrips() {
  const navigate = useNavigate();
  const trips = useMemo(() => loadTrips(), []);

  return (
    <main id="main" className="trips-page">
      <div className="page-ribbon" aria-hidden>
        <img src={`${IMAGES.split}&w=1200`} alt="" />
        <img src={`${IMAGES.hero}&w=800`} alt="" />
        <img src={`${IMAGES.city}&w=800`} alt="" />
        <img src={`${IMAGES.lakes}&w=800`} alt="" />
      </div>
      <div className="eyebrow">Library</div>
      <h1 style={{ fontSize: "3.4rem" }}>My trips</h1>
      <p className="muted">Saved on this device — open one like a travel journal.</p>
      {trips.length === 0 ? (
        <div className="panel empty" style={{ marginTop: 28 }}>
          <p>No saved journeys yet.</p>
          <Link className="btn btn-primary" to="/plan">
            Start planning
          </Link>
        </div>
      ) : (
        <div className="trip-grid" style={{ marginTop: 28 }}>
          {trips.map((trip) => (
            <article className="place-card" key={trip.id}>
              <img
                src={categoryImage(trip.featured_places[0]?.category || "attraction", trip.featured_places[0]?.photo_url)}
                alt=""
                style={{ height: 150, objectFit: "cover" }}
              />
              <div className="place-body">
                <h2 style={{ fontSize: "1.7rem", margin: 0 }}>{trip.title}</h2>
                <p className="muted">
                  {trip.preferences.duration_days} days · {trip.preferences.destination}
                </p>
                <p className="muted">
                  Created{" "}
                  {new Date(trip.created_at).toLocaleDateString("en-US", {
                    month: "short",
                    year: "numeric",
                  })}
                </p>
                <div className="actions-row">
                  <button className="btn btn-primary btn-small" type="button" onClick={() => navigate(`/trip/${trip.id}`)}>
                    Open trip
                  </button>
                  <button
                    className="btn btn-ghost btn-small"
                    type="button"
                    onClick={() => {
                      deleteTrip(trip.id);
                      navigate(0);
                    }}
                  >
                    Delete
                  </button>
                </div>
              </div>
            </article>
          ))}
        </div>
      )}
    </main>
  );
}
