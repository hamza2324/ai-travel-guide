import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { ATTRIBUTION, FIELD_NOTES, IMAGES, MOODS } from "../data";

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
          <video
            className="hero-video"
            autoPlay
            muted
            loop
            playsInline
            poster={IMAGES.hero}
          >
            <source src={IMAGES.video} type="video/mp4" />
          </video>
          <img className="hero-still" src={IMAGES.hero} alt="" />
        </div>
        <div className="hero-grain" aria-hidden />
        <div className="hero-overlay" />
        <div className="hero-content">
          <div className="eyebrow">Field companion · Karakoram to the cities</div>
          <h1>
            <em>Plan less.</em>
            <br />
            Travel like a guide.
          </h1>
          <p className="lead">
            Hour-by-hour days, distinct valleys, and a rupee budget that matches the road —
            not a copy-paste list repeated for a week.
          </p>
          <form
            className="hero-search"
            onSubmit={(event) => {
              event.preventDefault();
              start(prompt || "Plan a 7-day adventure trip to Hunza with mountains, photography, and food.");
            }}
          >
            <label htmlFor="hero-q" className="sr-only">
              Where do you want to go?
            </label>
            <input
              id="hero-q"
              value={prompt}
              onChange={(event) => setPrompt(event.target.value)}
              placeholder="Hunza for 7 days, two friends, mountains and food…"
            />
            <button className="btn btn-primary" type="submit">
              Begin the journey
            </button>
          </form>
          <div className="hero-pills">
            <span>Day-by-day corridors</span>
            <span>PKR field budget</span>
            <span>Adventure advice</span>
          </div>
        </div>
        <div className="hero-caption">Northern light · filmed in mountain air</div>
      </section>

      <section className="section filmstrip" aria-label="Destinations">
        {[IMAGES.hero, IMAGES.heroAlt, IMAGES.split, IMAGES.journal, IMAGES.moods.adventure, IMAGES.moods.history].map((src) => (
          <img key={src} src={`${src}&w=700`} alt="" loading="lazy" />
        ))}
      </section>

      <section className="section" id="discover">
        <div className="section-kicker">Explore by mood</div>
        <h2>Begin with a feeling, then follow a real route.</h2>
        <p className="muted" style={{ maxWidth: 540 }}>
          Each mood prefills the planner. The itinerary still changes by valley, hour, and drive time.
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

      <section className="section advisor-grid">
        <div>
          <div className="section-kicker">From the field book</div>
          <h2>Advice a local guide would actually give.</h2>
          <div className="advisor-list">
            {FIELD_NOTES.map((note) => (
              <article key={note.title} className="advisor-card">
                <h3>{note.title}</h3>
                <p className="muted">{note.body}</p>
              </article>
            ))}
          </div>
        </div>
        <div className="split-visual">
          <img src={IMAGES.journal} alt="High mountain road above a river valley" />
          <div className="split-caption">Keep one corridor per day. That is how the valley is walked.</div>
        </div>
      </section>

      <section className="section feature-grid">
        <div>
          <div className="section-kicker">How it thinks</div>
          <h2>A classical guide, with a modern engine.</h2>
          <div className="steps">
            <div>
              <div className="step-num">01 — Intent</div>
              <p className="muted">The model extracts destination, days, budget, and interests into structured data.</p>
            </div>
            <div>
              <div className="step-num">02 — Place discovery</div>
              <p className="muted">Live maps plus a verified northern-Pakistan field list: forts, lakes, cones, glaciers, passes.</p>
            </div>
            <div>
              <div className="step-num">03 — Day corridors</div>
              <p className="muted">Each day is a different geography. Hunza week: Karimabad, Altit, Attabad, Passu, Nagar, Gulmit, Khunjerab.</p>
            </div>
          </div>
        </div>
        <div className="split-visual">
          <img src={IMAGES.split} alt="Mountain valley at dusk" />
        </div>
      </section>

      <footer className="footer">
        <div>AI Travel Guide — a field companion for serious trips.</div>
        <div>{ATTRIBUTION}</div>
      </footer>
    </main>
  );
}
