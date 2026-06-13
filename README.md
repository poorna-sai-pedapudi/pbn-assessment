# PBN Assessment Starter

Full-stack starter application built with:

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- React
- Docker

## Project Structure

```text
backend/
frontend/
docker-compose.yml
```

## Backend Setup

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

Run backend:

```bash
uvicorn app.main:app --reload
```

Backend available at:

```text
http://localhost:8000
```

Swagger Docs:

```text
http://localhost:8000/docs
```

---

## Database Setup

Start PostgreSQL:

```bash
docker compose up -d
```

Run migrations:

```bash
alembic upgrade head
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend available at:

```text
http://localhost:5173
```

---

## Running Tests

```bash
pytest
```

Expected:

```text
1 passed
```

---

## Features

- Create Item
- List Items
- Delete Item
- PostgreSQL Persistence
- Alembic Migrations
- Health Check Endpoint

## Health Check

```text
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```


## Deployment Strategy

For production, the backend can be deployed as a Dockerized FastAPI service on Render, Railway, or AWS ECS. The React frontend can be built as static assets and deployed through Vercel, Netlify, or CloudFront. PostgreSQL should run as a managed database.

Alembic migrations should run during the release process before the application starts. The `/health` endpoint can be used by a load balancer or hosting platform to verify backend readiness.

Production additions would include TLS, secrets management, automated backups, monitoring, audit logging, and environment-specific configuration.

## Tradeoffs / Future Improvements

To be updated based on the actual assessment requirements.