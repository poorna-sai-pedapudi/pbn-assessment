# PBN Assessment — Auto Repair Shop Booking

Full-stack appointment booking system for an auto repair shop. Customers browse available time slots and book appointments; the provider view lists all upcoming bookings; a dashboard shows booking analytics.

**Stack:** FastAPI · PostgreSQL · SQLAlchemy · Alembic · React 19 · Vite · Docker

## Project Structure

```text
backend/          FastAPI application, SQLAlchemy models, Alembic migrations
  app/
    routers/      services, mechanics, working_hours, appointments, stats
    models.py     ORM models (Service, Mechanic, WorkingHours, Appointment)
    schemas.py    Pydantic request/response schemas
    crud.py       Database query helpers
    main.py       FastAPI app entry point with CORS config
  alembic/        Migration scripts
  requirements.txt
frontend/         React + Vite SPA
  src/
    CustomerView.jsx
    ProviderView.jsx
    DashboardView.jsx
    api/api.js
docker-compose.yml  Runs PostgreSQL 16 on port 5433
```

## Prerequisites

- Python 3.11+
- Node.js v20+ / npm 11+
- Docker (for PostgreSQL)

## Environment Variables

Copy the example and adjust if needed:

```bash
cp backend/.env.example backend/.env
```

Default `.env`:

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/pbn_db
```

## Database Setup

```bash
docker compose up -d
```

PostgreSQL runs on port **5433** (mapped from container 5432) to avoid clashing with a local Postgres install.

Run migrations:

```bash
cd backend
alembic upgrade head
```

## Backend Setup

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend available at:

```
http://localhost:8000
```

Swagger / OpenAPI docs:

```
http://localhost:8000/docs
```

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend available at:

```
http://localhost:5173
```

## Running Tests

```bash
cd backend
pytest
```

Expected output:

```
1 passed
```

## Health Check

```
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```


## Deployment Strategy

### Overview

The application has three independently deployable units:

| Unit | Artifact | Suggested target |
|------|----------|-----------------|
| PostgreSQL | Managed DB | Render Postgres, AWS RDS, Supabase |
| FastAPI backend | Docker image | Render Web Service, Railway, AWS ECS/Fargate |
| React frontend | Static files (`dist/`) | Vercel, Netlify, AWS S3 + CloudFront |

---

### 1. Database

Use a managed PostgreSQL 16 instance. At release time, run Alembic migrations before the new backend version starts taking traffic:

```bash
alembic upgrade head
```

This is safe to run as a one-off pre-deploy step or as a release command in Render/Railway. The migration history in `alembic/versions/` tracks schema state; `create_all` is intentionally not called at startup.

---

### 2. Backend (Docker)

A minimal `Dockerfile` for the backend:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run locally:

```bash
docker build -t pbn-backend ./backend
docker run -p 8000:8000 -e DATABASE_URL=... pbn-backend
```

**Environment variables required in production:**

| Variable | Example |
|----------|---------|
| `DATABASE_URL` | `postgresql://user:pass@host:5432/dbname` |

The `/health` endpoint (`GET /health`) should be configured as the health-check path on any load balancer or hosting platform. It returns `{"status": "healthy"}` with HTTP 200 when the app is ready.

**CORS:** Update the `allow_origins` list in [backend/app/main.py](backend/app/main.py) to include the production frontend domain before deploying.

---

### 3. Frontend (Static)

```bash
cd frontend
VITE_API_BASE_URL=https://your-backend-domain.com npm run build
```

> The `VITE_API_BASE_URL` env variable must be consumed in `src/api/api.js` — update the base URL reference there to use `import.meta.env.VITE_API_BASE_URL` before deploying.

The `dist/` directory contains a single-page app. Deploy it to any static host:

- **Vercel / Netlify:** connect the repo, set `VITE_API_BASE_URL`, build command `npm run build`, publish dir `dist`.
- **AWS S3 + CloudFront:** sync `dist/` to an S3 bucket, enable static website hosting, add a CloudFront distribution in front. Add a CloudFront error page rule to return `index.html` for 404s so client-side routing works.

---

### 4. CI/CD (suggested pipeline)

```
push to main
  └─ run pytest (backend)
  └─ run eslint (frontend)
  └─ docker build + push image to registry
  └─ run: alembic upgrade head   ← pre-deploy migration
  └─ deploy new image to hosting platform
  └─ build & deploy frontend static assets
```

---

### Production checklist

- [ ] TLS/HTTPS on both backend and frontend domains
- [ ] `DATABASE_URL` and any secrets stored in platform secret store (not in env files)
- [ ] CORS `allow_origins` restricted to the production frontend URL
- [ ] Automated PostgreSQL backups enabled on the managed DB
- [ ] Health-check path `/health` configured on the load balancer
- [ ] Monitoring / alerting (e.g. Sentry for errors, Datadog or platform metrics for latency)
- [ ] Audit logging for appointment create/cancel events

## Architecture Notes & Tradeoffs

### Design decisions
- **Availability is computed, not stored.** Slots are generated on-demand from each mechanic's working hours minus existing appointments, rather than pre-generating a slot table. This keeps the data model small and avoids stale slot records when bookings change.
- **Appointment end time is derived server-side** from the service's duration, not sent by the client. This keeps a single source of truth and prevents inconsistent records.
- **Alembic owns the schema.** `create_all` was removed so migrations are the only path to schema changes — closer to how a real deployment manages the database.
- **Overlap detection** uses the standard interval rule (`start_a < end_b AND start_b < end_a`), which cleanly handles partial overlaps, full containment, and varying service durations.
- **Prices stored as whole-dollar integers** for the prototype. In production I'd use integer cents or a fixed-precision decimal type to avoid floating-point rounding on money.

### Scoped out for the time-box (would add next)
- **Authentication & route separation.** The customer and provider experiences are currently a single-page toggle. In production these are different audiences with different trust levels — the provider view exposes all customers' bookings, so it needs to be a protected, role-based route. Splitting into authenticated routes is the first thing I'd add.
- **Server-side conflict check on booking.** The availability endpoint only offers free slots, but the create endpoint trusts the client. I'd add an overlap re-check at booking time to prevent double-booking under concurrent requests.
- **Service-to-mechanic mapping.** Currently any mechanic can perform any service. A join table would model which staff are qualified for which services.
- **Configurable slot interval and buffers.** The 30-minute step is hardcoded; real shops need per-service intervals and buffer time between jobs (e.g. cleanup between brake jobs).
- **CRUD completeness.** Update/delete on services, mechanics, and working hours were scoped out since they don't appear in the required user journeys.

### With more time
- Provider dashboard with booking insights (most-requested services, peak times).
- Pagination and filtering on the appointments list.
- Frontend test coverage and more backend tests beyond the health check.
- Timezone handling for multi-location businesses.


## Versions

node - v20.18.0
npm - 11.11.0