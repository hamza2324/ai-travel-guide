const STEPS = [
  "Understanding your travel style...",
  "Discovering places you'll love...",
  "Analyzing distances...",
  "Building an efficient route...",
  "Creating your personalized journey...",
];

export function LoadingJourney({ step }: { step: number }) {
  const label = STEPS[Math.min(step, STEPS.length - 1)];
  return (
    <div className="loading-screen" role="status" aria-live="polite">
      <div>
        <div className="eyebrow">Planning in progress</div>
        <h2>{label}</h2>
        <p className="muted">The model extracts intent. Location data and scoring build the route.</p>
        <div className="progress-track">
          <div className="progress-bar" />
        </div>
      </div>
    </div>
  );
}
