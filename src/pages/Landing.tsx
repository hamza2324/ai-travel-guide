import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { ATTRIBUTION, IMAGES, MOODS } from "../data";

export function Landing() {
  const navigate = useNavigate();
  const [prompt, setPrompt] = useState("");

  function start(text?: string, mood?: { interests: string[]; style: string; label: string }) {
    const params = new URLSearchParams();
    if (text) params.set("q", text);
    if (mood) {
      params.set("interests", mood.interests.join(","));
      params.set("style", mood.style);
      params.set("mood", mood.label);
    }
    navigate(`/plan?${params.toString()}`);
  }

  return (
    <main id="main">
      <section className="hero">
        <div className="hero-media" aria-hidden>
          <img src={IMAGES.hero} alt="" />
        </div>
        <div className="hero-overlay" />
        <div className="hero-content">
          <div className="eyebrow">AI-powered travel companion</div>
          <h1>
            Plan less.
            <br />
            Experience more.
          </h1>
          <p className="lead">
            Your AI-powered travel companion creates personalized trips based on your interests,
            budget, location, and time.
          </p>
          <form
            className="hero-search"
            onSubmit={(event) => {
              event.preventDefault();
              start(prompt || "Plan a 3-day trip with nature, food, and photography.");
            }}
          >
            <label className="visually-hidden" htmlFor="hero-q" style={{ position: "absolute", left: -9999 }}>
              Where do you want to go?
            </label>
            <input
              id="hero-q"
              value={prompt}
              onChange={(event) => setPrompt(event.target.value)}
              placeholder="Where do you want to go?"
            />
            <button className="btn btn-primary" type="submit">
              Start planning
            </button>
          </form>
          <div className="hero-pills">
            <span>🌍 Personalized</span>
            <span>🧠 AI powered</span>
            <span>📍 Location aware</span>
          </div>
        </div>
      </section>

      <section className="section" id="discover">
        <div className="section-kicker">Explore by mood</div>
        <h2>Begin with a feeling, not a spreadsheet.</h2>
        <p className="muted" style={{ maxWidth: 520 }}>
          Choose a mood and we prefill a planner that still listens to natural language.
        </p>
        <div className="mood-grid">
          {MOODS.map((mood) => (
            <button key={mood.id} className="mood-card" type="button" onClick={() => start(undefined, mood)}>
              <img src={mood.image} alt="" loading="lazy" />
              <span>{mood.label}</span>
            </button>
          ))}
        </div>
      </section>

      <section className="section feature-grid">
        <div>
          <div className="section-kicker">How it thinks</div>
          <h2>Intelligence in the architecture, not just a chat box.</h2>
          <div className="steps">
            <div>
              <div className="step-num">01 — Intent</div>
              <p className="muted">Llama 3.3 70B extracts destination, duration, budget, and interests into structured data.</p>
            </div>
            <div>
              <div className="step-num">02 — Place discovery</div>
              <p className="muted">Live map data finds viewpoints, museums, parks, and restaurants around the destination.</p>
            </div>
            <div>
              <div className="step-num">03 — Scoring + routes</div>
              <p className="muted">A deterministic engine ranks matches, groups nearby stops, and builds a realistic day plan.</p>
            </div>
          </div>
        </div>
        <div className="split-visual">
          <img src={IMAGES.split} alt="Mountain valley at dusk" />
        </div>
      </section>

      <footer className="footer">
        <div>AI Travel Guide — a portfolio travel intelligence product.</div>
        <div>{ATTRIBUTION}</div>
      </footer>
    </main>
  );
}
