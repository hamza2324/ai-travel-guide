import { IMAGES } from "../data";

const STEPS = [
  "Reading the trip you described...",
  "Gathering places that actually belong there...",
  "Laying out each day as its own corridor...",
  "Checking drive time and light...",
  "Writing a route you can follow tomorrow...",
];

export function LoadingJourney({ step }: { step: number }) {
  const label = STEPS[Math.min(step, STEPS.length - 1)];
  return (
    <div className="loading-screen" role="status" aria-live="polite">
      <img className="loading-bg" src={IMAGES.heroAlt} alt="" />
      <div className="loading-veil" aria-hidden />
      <div className="loading-copy">
        <div className="eyebrow">Your itinerary is taking shape</div>
        <h2>{label}</h2>
        <p className="muted">A few seconds of mapping — then a day-by-day plan, not a generic list.</p>
        <div className="progress-track">
          <div className="progress-bar" />
        </div>
      </div>
    </div>
  );
}
