import { FormEvent, useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";
import { api } from "../api";
import { LocationSearch } from "../components/LocationSearch";
import { LoadingJourney } from "../components/LoadingJourney";
import { IMAGES } from "../data";
import { INTERESTS, type BudgetTier, type GeoPoint, type TravelStyle, type TravelerType } from "../types";
import { cacheDraft, saveTrip } from "../storage";

export function Planner() {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const [mode, setMode] = useState<"natural" | "guided">("natural");
  const [prompt, setPrompt] = useState(params.get("q") || "");
  const [destination, setDestination] = useState("");
  const [origin, setOrigin] = useState("");
  const [originCoords, setOriginCoords] = useState<GeoPoint | undefined>();
  const [duration, setDuration] = useState(3);
  const [budget, setBudget] = useState<BudgetTier>("moderate");
  const [style, setStyle] = useState<TravelStyle>((params.get("style") as TravelStyle) || "balanced");
  const [travelers, setTravelers] = useState<TravelerType>("friends");
  const [interests, setInterests] = useState<string[]>(
    params.get("interests")?.split(",").filter(Boolean) || ["nature", "food"]
  );
  const [busy, setBusy] = useState(false);
  const [step, setStep] = useState(0);
  const [error, setError] = useState("");
  const [geoNote, setGeoNote] = useState("");

  const mood = params.get("mood");

  useEffect(() => {
    if (mood && !prompt) {
      setPrompt(`Plan a ${style} trip focused on ${mood.toLowerCase()}.`);
    }
  }, [mood, prompt, style]);

  const examples = useMemo(
    () => [
      "Plan a 3-day budget-friendly trip to Islamabad for two friends. We love mountains, food, photography, and historical places.",
      "I am currently in Abbottabad. Suggest a one-day scenic trip nearby.",
      "Plan a relaxing family trip with minimal driving.",
    ],
    []
  );

  function toggleInterest(value: string) {
    setInterests((current) =>
      current.includes(value) ? current.filter((item) => item !== value) : [...current, value]
    );
  }

  async function useCurrentLocation() {
    setGeoNote("");
    if (!navigator.geolocation) {
      setGeoNote("Location is not available in this browser.");
      return;
    }
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const coords = { lat: position.coords.latitude, lng: position.coords.longitude };
        setOriginCoords(coords);
        try {
          const response = await fetch(`/api/places/reverse?lat=${coords.lat}&lng=${coords.lng}`);
          const data = await response.json();
          setOrigin(data.label || "Current location");
        } catch {
          setOrigin("Current location");
        }
      },
      () => setGeoNote("Location permission was denied. You can enter a starting city instead.")
    );
  }

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setError("");
    if (mode === "natural" && prompt.trim().length < 8 && !destination) {
      setError("Tell us a little more about the trip you want.");
      return;
    }
    if (mode === "guided" && destination.trim().length < 2 && !prompt) {
      setError("Choose a destination or describe the trip in natural language.");
      return;
    }
    setBusy(true);
    setStep(0);
    const timer = window.setInterval(() => setStep((value) => Math.min(value + 1, 4)), 1400);
    try {
      const result = await api.plan({
        natural_language: prompt.trim() || undefined,
        destination: destination.trim() || undefined,
        origin: origin.trim() || undefined,
        origin_coords: originCoords,
        duration_days: mode === "guided" ? duration : undefined,
        budget,
        travel_style: style,
        travelers,
        interests,
      });
      cacheDraft(result.trip);
      saveTrip(result.trip);
      sessionStorage.setItem("ai-travel-guide.warnings", JSON.stringify(result.warnings || []));
      navigate(`/trip/${result.trip.id}`, { state: { trip: result.trip, warnings: result.warnings } });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Planning failed. Please try again.");
    } finally {
      window.clearInterval(timer);
      setBusy(false);
    }
  }

  if (busy) {
    return (
      <main id="main" className="planner-page">
        <LoadingJourney step={step} />
      </main>
    );
  }

  return (
    <main id="main" className="planner-page">
      <div className="page-ribbon" aria-hidden>
        <img src={`${IMAGES.hero}&w=1200`} alt="" />
        <img src={`${IMAGES.lakes}&w=800`} alt="" />
        <img src={`${IMAGES.table}&w=800`} alt="" />
        <img src={`${IMAGES.city}&w=800`} alt="" />
      </div>
      <div className="planner-shell">
        <motion.form
          className="panel"
          onSubmit={onSubmit}
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45 }}
        >
          <div className="eyebrow">Trip planner</div>
          <h1 style={{ fontSize: "3.2rem", marginBottom: 8 }}>Describe the journey.</h1>
          <p className="muted">
            Write it the way you’d text a friend. We’ll turn it into days, photos, and a map — then you can swap stops.
          </p>
          <div className="mode-toggle" role="tablist" aria-label="Planning mode">
            <button type="button" className={mode === "natural" ? "active" : ""} onClick={() => setMode("natural")}>
              Natural language
            </button>
            <button type="button" className={mode === "guided" ? "active" : ""} onClick={() => setMode("guided")}>
              Guided
            </button>
          </div>

          {mode === "natural" ? (
            <>
              <label htmlFor="nl" className="muted">
                Your request
              </label>
              <textarea
                id="nl"
                className="nl-input"
                value={prompt}
                onChange={(event) => setPrompt(event.target.value)}
                placeholder={examples[0]}
              />
              <div className="chips" style={{ marginTop: 12 }}>
                {examples.map((item) => (
                  <button key={item} type="button" className="chip" onClick={() => setPrompt(item)}>
                    {item.slice(0, 42)}…
                  </button>
                ))}
              </div>
            </>
          ) : (
            <>
              <LocationSearch
                id="destination"
                label="Destination"
                value={destination}
                placeholder="Islamabad, Hunza, Kyoto…"
                onChange={setDestination}
              />
              <LocationSearch
                id="origin"
                label="Starting location"
                value={origin}
                placeholder="City or neighborhood"
                onChange={(value) => {
                  setOrigin(value);
                  setOriginCoords(undefined);
                }}
                onSelect={(item) => item.coords && setOriginCoords(item.coords)}
              />
              <button type="button" className="btn btn-ghost btn-small" onClick={useCurrentLocation}>
                Use current location
              </button>
              {geoNote && <p className="muted">{geoNote}</p>}
              <div className="field">
                <label htmlFor="duration">Duration</label>
                <select id="duration" value={duration} onChange={(event) => setDuration(Number(event.target.value))}>
                  <option value={1}>One day</option>
                  <option value={2}>Weekend</option>
                  <option value={3}>3 days</option>
                  <option value={5}>5 days</option>
                  <option value={7}>7 days</option>
                </select>
              </div>
              <div className="field">
                <label htmlFor="nl2">Anything else to add?</label>
                <textarea
                  id="nl2"
                  className="nl-input"
                  style={{ minHeight: 80 }}
                  value={prompt}
                  onChange={(event) => setPrompt(event.target.value)}
                  placeholder="Optional: dietary needs, pace, or a place you must see."
                />
              </div>
            </>
          )}

          <div className="field" style={{ marginTop: 18 }}>
            <label>Budget</label>
            <div className="chips">
              {(["budget", "moderate", "premium"] as BudgetTier[]).map((item) => (
                <button key={item} type="button" className={`chip ${budget === item ? "active" : ""}`} onClick={() => setBudget(item)}>
                  {item}
                </button>
              ))}
            </div>
          </div>
          <div className="field">
            <label>Travel style</label>
            <div className="chips">
              {(["relaxed", "balanced", "fast-paced"] as TravelStyle[]).map((item) => (
                <button key={item} type="button" className={`chip ${style === item ? "active" : ""}`} onClick={() => setStyle(item)}>
                  {item}
                </button>
              ))}
            </div>
          </div>
          <div className="field">
            <label>Traveling with</label>
            <div className="chips">
              {(["solo", "friends", "family", "couple"] as TravelerType[]).map((item) => (
                <button
                  key={item}
                  type="button"
                  className={`chip ${travelers === item ? "active" : ""}`}
                  onClick={() => setTravelers(item)}
                >
                  {item}
                </button>
              ))}
            </div>
          </div>
          <div className="field">
            <label>Interests</label>
            <div className="chips">
              {INTERESTS.map((item) => (
                <button
                  key={item}
                  type="button"
                  className={`chip ${interests.includes(item) ? "active" : ""}`}
                  onClick={() => toggleInterest(item)}
                >
                  {item}
                </button>
              ))}
            </div>
          </div>

          {error && <div className="alert">{error}</div>}
          <button className="btn btn-primary" type="submit" style={{ marginTop: 12, width: "100%" }}>
            Build my itinerary
          </button>
        </motion.form>
        <aside className="panel planner-aside">
          <div className="planner-collage" aria-hidden>
            <img src={`${IMAGES.heroAlt}&w=900`} alt="" />
            <img src={`${IMAGES.journal}&w=700`} alt="" />
            <img src={`${IMAGES.table}&w=700`} alt="" />
          </div>
          <div className="planner-aside-copy">
            <div className="section-kicker">What you get</div>
            <h2 style={{ fontSize: "2.4rem" }}>A day-by-day route, not a listicle.</h2>
            <p className="muted">
              Each stop has a photo, visit time, and why it belongs on that day. Switch days on the map. Ask to swap a
              museum for a viewpoint.
            </p>
            <ul className="planner-perks">
              <li>
                <b>—</b> Distinct corridors so Hunza doesn’t repeat the same fort all week
              </li>
              <li>
                <b>—</b> Drive time baked into the schedule
              </li>
              <li>
                <b>—</b> Budget quoted in PKR, not a made-up dollar guess
              </li>
              <li>
                <b>—</b> A map you can follow, stop by stop
              </li>
            </ul>
          </div>
        </aside>
      </div>
    </main>
  );
}
