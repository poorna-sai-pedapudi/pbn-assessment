# PBN Assessment — Frontend

React single-page application for the auto repair shop appointment booking system, built with Vite.

## Tech Stack

- React 19
- Vite 5
- Recharts (analytics dashboard)
- ESLint with react-hooks and react-refresh plugins

## Prerequisites

- Node.js v20+
- npm 11+

## Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

The dev server proxies nothing — the React app talks directly to the backend at `http://localhost:8000`. Make sure the backend is running before using the UI.

## Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start Vite dev server with HMR |
| `npm run build` | Production build to `dist/` |
| `npm run preview` | Serve the production build locally |
| `npm run lint` | Run ESLint |

## Project Structure

```
src/
  App.jsx              # Root component — view switcher (Customer / Provider / Dashboard)
  CustomerView.jsx     # Customer booking flow (select service, mechanic, slot → book)
  ProviderView.jsx     # Provider view — lists all upcoming appointments
  DashboardView.jsx    # Analytics charts (appointments by service, mechanic, day)
  api/
    api.js             # All fetch calls to the FastAPI backend
  main.jsx             # React entry point
```

## Views

**Customer** — select a service and mechanic, pick an available time slot, and submit a booking.

**Provider** — read-only list of all upcoming appointments across all mechanics.

**Dashboard** — charts showing appointment volume by service, mechanic, and day of the week using Recharts.

## Environment

The backend base URL is hardcoded to `http://localhost:8000` in [src/api/api.js](src/api/api.js). For production, set `VITE_API_BASE_URL` as an env variable and update `api.js` accordingly.

## Production Build

```bash
npm run build
```

Output lands in `dist/`. Deploy the `dist/` folder to any static host (Vercel, Netlify, S3/CloudFront). Set the `VITE_API_BASE_URL` env variable at build time to point to the production backend.
