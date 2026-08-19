import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { motion } from "framer-motion";
import { ATTRIBUTION, DESTINATIONS, FIELD_NOTES, FILMSTRIP, IMAGES, MOODS } from "../data";

const fade = {
  hidden: { opacity: 0, y: 28 },
  show: { opacity: 1, y: 0, transition: { duration: 0.7, ease: [0.22, 1, 0.36, 1] } },
};

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

  const strip = [...FILMSTRIP, ...FILMSTRIP];

  return (
    <main id="main">
      <section className="hero">
        <div className="hero-media" aria-hidden>
          <video className="hero-video" autoPlay muted loop playsInline poster={IMAGES.hero}>
            <source src={IMAGES.video} type="video/mp4" />
          </video>
          <img className="hero-still" src={IMAGES.hero} alt="" />
        </div>
        <div className="hero-grain" aria-hidden />
        <div className="hero-overlay" />
        <motion.div className="hero-content" initial="hidden" animate="show" variants={fade}>
          <div className="eyebrow">A quieter way to plan · Karakoram to the cities</div>
          <h1>
            <em>Where next?</em>
            <br />
            We’ll map the days.
          </h1>
          <p className="lead">
            Tell us the trip in plain language. Get a photo-rich, hour-by-hour route with a rupee budget —
            the kind of plan a good local guide would sketch.
          </p>
          <form
            className="hero-search"
            onSubmit={(event) => {
              event.preventDefault();
              start(prompt || DESTINATIONS[0].query);
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
              Start planning
            </button>
          </form>
          <div className="hero-pills">
            <span>Day-by-day corridors</span>
            <span>PKR field budget</span>
            <span>Live map + photos</span>
          </div>
        </motion.div>
        <div className="hero-caption">Northern light · filmed in mountain air</div>
      </section>

      <section className="section filmstrip" aria-label="Destinations">
        <div className="filmstrip-track">
          {strip.map((src, index) => (
            <img key={`${src}-${index}`} src={`${src}&w=700`} alt="" loading="lazy" />
          ))}
        </div>
      </section>

      <motion.section
        className="section"
        initial="hidden"
        whileInView="show"
        viewport={{ once: true, amount: 0.2 }}
        variants={fade}
      >
        <div className="section-kicker">Popular journeys</div>
        <h2>Start from a place, not a form.</h2>
        <p className="muted" style={{ maxWidth: 540 }}>
          Tap a destination the way you would in a travel magazine — then refine budget, pace, and company.
        </p>
        <div className="dest-grid">
          {DESTINATIONS.map((place) => (
            <button key={place.name} className="dest-card" type="button" onClick={() => start(place.query)}>
              <img src={`${place.image}&w=900`} alt="" loading="lazy" />
              <div className="dest-copy">
                <small>{place.line}</small>
                <h3>{place.name}</h3>
              </div>
            </button>
          ))}
        </div>
      </motion.section>

      <motion.section
        className="section"
        id="discover"
        initial="hidden"
        whileInView="show"
        viewport={{ once: true, amount: 0.2 }}
        variants={fade}
      >
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
      </motion.section>

      <motion.section
        className="section advisor-grid"
        initial="hidden"
        whileInView="show"
        viewport={{ once: true, amount: 0.2 }}
        variants={fade}
      >
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
      </motion.section>

      <motion.section
        className="section feature-grid"
        initial="hidden"
        whileInView="show"
        viewport={{ once: true, amount: 0.2 }}
        variants={fade}
      >
        <div>
          <div className="section-kicker">How the days get built</div>
          <h2>Less typing. More of the trip.</h2>
          <div className="steps">
            <div>
              <div className="step-num">01 — You describe it</div>
              <p className="muted">A sentence is enough: where, how long, who you’re with, what you care about.</p>
            </div>
            <div>
              <div className="step-num">02 — Places, not placeholders</div>
              <p className="muted">Live maps plus a verified northern-Pakistan field list: forts, lakes, cones, glaciers, passes.</p>
            </div>
            <div>
              <div className="step-num">03 — A route you can walk</div>
              <p className="muted">Each day is a different geography, timed for light and drive — then shown on a map.</p>
            </div>
          </div>
        </div>
        <div className="split-visual">
          <img src={IMAGES.split} alt="Mountain valley at dusk" />
        </div>
      </motion.section>

      <footer className="footer">
        <div>AI Travel Guide — planned like a magazine, walked like a map.</div>
        <div>{ATTRIBUTION}</div>
      </footer>
    </main>
  );
}
