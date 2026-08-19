# AI Travel Guide

A FastAPI + React travel planner that turns a natural-language request into a **day-by-day, route-aware itinerary** with photos, a map, and a **PKR field budget**. It is not a chatbot wrapper: the model extracts structured intent; place discovery, scoring, and scheduling are deterministic.

Built as a portfolio product for travelers who want a usable route — especially in northern Pakistan — rather than a copy-pasted list of the same landmarks every day.

## Overview

Describe a trip (destination, length, budget, company, interests). The app geocodes the destination, discovers places (OpenStreetMap by default, Google Places if a server key is set), scores them, clusters **distinct day corridors**, and returns an itinerary you can edit with a trip assistant. Trips are saved in the browser (`localStorage`).

## Features

- Natural-language planner plus a guided form (budget, pace, travelers, interests)
- Structured intent extraction (JSON validated with Pydantic; not raw model output)
- Place discovery with curated fallbacks for destinations such as Hunza, Islamabad, Lahore, and Skardu
- Unique day corridors so a 7-day Hunza plan does not repeat the same fort
- Leaflet map (CARTO Voyager tiles) with day switching
- Estimated **PKR** budget ranges (guesthouse / meals / jeep-style field rates — estimates, not invoices)
- In-app assistant that applies structured edits (`replace`, `less driving`, and similar actions)
- Light editorial UI (cream paper, photography, motion) with a cinematic landing hero

## How it works

```text
User request
      ↓
Intent JSON (Llama 3.3 70B via OpenRouter, Groq preferred)
      ↓
Geocoding + place discovery (OSM / Overpass, or Google Places)
      ↓
Deterministic scoring (interest, rating, distance, budget, fit)
      ↓
Day corridors → nearest-neighbor order → 2-opt cleanup → meals
      ↓
PKR budget estimate + narrative copy
      ↓
React trip dashboard (map, timeline, assistant)
```

The assistant does not rewrite the whole trip as free text. It returns structured actions that the itinerary engine applies.

## Technology stack

| Layer | Stack |
| --- | --- |
| Frontend | React 19, Vite, TypeScript, React Router, Leaflet, Framer Motion |
| Backend | Python, FastAPI, Pydantic v2, httpx, SlowAPI |
| AI | OpenRouter → `meta-llama/llama-3.3-70b-instruct` (provider order Groq) |
| Maps | Leaflet + CARTO Voyager; OSRM driving times; Nominatim / Overpass; optional Google Maps Platform |

## Project structure

```text
index.html          Vite app entry (repository root)
src/                React pages and components
backend/            FastAPI, AI, places, itinerary, budget
run.py              API launcher (reads APP_PORT from .env)
start.bat           Windows helper to start the stack
.env.example        Environment template (no secrets)
```

## Installation

Requires Python 3.11+ and Node.js 18+.

```bash
git clone https://github.com/hamza2324/ai-travel-guide.git
cd ai-travel-guide
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r backend/requirements.txt
npm install
```

macOS / Linux:

```bash
source .venv/bin/activate
pip install -r backend/requirements.txt
npm install
```

## Configuration

Copy `.env.example` to `.env` at the **repository root**. Never commit `.env`.

| Variable | Required | Purpose |
| --- | --- | --- |
| `OPENROUTER_API_KEY` | Yes (for live AI) | LLM access |
| `OPENROUTER_MODEL` | No | Default `meta-llama/llama-3.3-70b-instruct` |
| `OPENROUTER_PROVIDER` | No | Default `Groq` |
| `APP_PORT` | No | Default `8010` in `.env.example` |
| `GOOGLE_MAPS_API_KEY` | No | Server-side Places / geocode / distance |
| `CORS_ORIGINS` | No | Comma-separated browser origins |

Without a Google key, planning still uses Nominatim, Overpass, OSRM, and curated place seeds.

## Usage

Terminal 1 — API:

```bash
python run.py
```

Health check: [http://127.0.0.1:8010/api/health](http://127.0.0.1:8010/api/health)

Terminal 2 — UI:

```bash
npm run dev
```

App: [http://localhost:5173](http://localhost:5173) (Vite may pick 5174/5175 if 5173 is busy). `/api` is proxied to FastAPI.

After `npm run build`, FastAPI can also serve `dist/` from `/`.

On Windows, `start.bat` can launch the stack.

## API

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/health` | Liveness, AI enabled flag, model/provider |
| POST | `/api/trips/plan` | Build an itinerary (rate-limited) |
| POST | `/api/trips/modify` | Apply a structured assistant edit |
| POST | `/api/ai/analyze-request` | Intent extraction only |
| GET | `/api/places/search` | Location autocomplete |
| GET | `/api/places/geocode` | Forward geocode |
| GET | `/api/places/reverse` | Reverse geocode |
| POST | `/api/itinerary/generate` | Same planning pipeline as `/api/trips/plan` |

Interactive docs when the API is running: [http://127.0.0.1:8010/docs](http://127.0.0.1:8010/docs)

## Limitations

- Live planning needs `OPENROUTER_API_KEY` and a reachable backend; a static frontend alone cannot call Groq.
- Place coverage depends on OSM/Overpass (or Google) plus curated seeds — not a complete worldwide catalogue.
- PKR figures are field-style ranges, not live quotes.
- Trips are device-local (`localStorage`); there is no account system.

## Future improvements

- Accounts and shared trips
- Weather-aware day shuffling
- PDF / ICS export
- Deeper restaurant and hotel clustering

Photography via Unsplash. Hero video via Pexels. Map data © OpenStreetMap contributors. Routing via OSRM.
