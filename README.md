# Expense Intelligence

Expense Intelligence is a full-stack personal finance dashboard for tracking expenses, monitoring budgets, and generating practical spending insights from transaction history.

The application is split into:

- A FastAPI backend for authentication, transactions, budgets, analytics, and chat-style insight responses
- A React and Vite frontend for the dashboard experience
- A PostgreSQL database, currently designed to work well with Supabase

## Highlights

- JWT-based authentication with Argon2 password hashing
- Transaction capture with merchant, category, payment mode, and date
- Budget tracking with projected overspend warnings
- Insight generation for category breakdowns, trends, anomalies, and recurring subscriptions
- Chat endpoint for quick finance questions based on the user's own data
- Deployment-ready setup for Vercel, Render, and Supabase

## Tech Stack

### Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- Gunicorn with Uvicorn workers
- Pydantic

### Frontend

- React 19
- TypeScript
- Vite
- Axios
- Recharts

### Infrastructure

- Vercel for the frontend
- Render for the backend
- Supabase Postgres for the database

## Repository Structure

```text
expense-intelligence/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   ├── tests/
│   ├── .env.example
│   ├── Procfile
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── public/
│   ├── src/
│   ├── .env.example
│   ├── package.json
│   └── vite.config.ts
├── .gitignore
├── render.yaml
└── README.md
```

## API Overview

### Authentication

- `POST /auth/register`
- `POST /auth/login`

### Transactions

- `POST /transactions/`
- `GET /transactions/`

### Insights

- `GET /insights/`

### Budget

- `POST /budget/`

### Chat

- `POST /chat/`

Interactive API docs are available at `/docs` when the backend is running.

## Local Development

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

On Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python run.py
```

Backend default URL:

```text
http://localhost:8000
```

### 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Frontend default URL:

```text
http://localhost:5173
```

### 3. Local Integration

Set the frontend API URL in `frontend/.env.local`:

```env
VITE_API_URL=http://localhost:8000
```

## Environment Variables

### Backend

Use `backend/.env.example` as the source of truth.

Key variables:

```env
DATABASE_URL=postgresql://postgres.<project-ref>:[YOUR-PASSWORD]@aws-0-<region>.pooler.supabase.com:5432/postgres
INIT_DB_ON_STARTUP=False
SECRET_KEY=change-this-to-a-secure-random-key-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DEBUG=False
CORS_ORIGIN=http://localhost:5173,https://your-production-domain.vercel.app
CORS_ORIGIN_REGEX=^https?://(localhost|127\.0\.0\.1)(:\d+)?$|^https://.*\.vercel\.app$
```

### Frontend

```env
VITE_API_URL=http://localhost:8000
```

## Deployment

### Recommended Production Topology

- Frontend: Vercel
- Backend: Render
- Database: Supabase session pooler

### Frontend on Vercel

Project settings:

- Framework preset: `Vite`
- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`

Required environment variable:

```env
VITE_API_URL=https://your-render-service.onrender.com
```

### Backend on Render

This repository includes `render.yaml` for Render Blueprint deployment.

Important Render configuration:

- Root directory: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn -k uvicorn.workers.UvicornWorker app.main:app`

Required environment variables:

```env
DATABASE_URL=<supabase-session-pooler-url>
INIT_DB_ON_STARTUP=False
SECRET_KEY=<strong-random-secret>
DEBUG=False
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGIN=https://your-vercel-app.vercel.app
CORS_ORIGIN_REGEX=^https?://(localhost|127\.0\.0\.1)(:\d+)?$|^https://.*\.vercel\.app$
```

### Supabase

Use the session pooler connection string for hosted deployments. This avoids the IPv6 connectivity issues that can happen with the direct database host on some platforms.

Format:

```env
postgresql://postgres.<project-ref>:[YOUR-PASSWORD]@aws-0-<region>.pooler.supabase.com:5432/postgres
```

## Testing

Backend tests live under `backend/tests`.

Run:

```bash
cd backend
pytest
```

The test suite uses a local SQLite database so it does not depend on your production Postgres instance.

## Production Readiness Notes

- The backend startup respects platform-provided `PORT`
- The Render start command uses ASGI-compatible workers
- CORS is configured for local development plus Vercel preview and production deployments
- Local environment files, virtual environments, caches, and build artifacts are ignored
- The repository now keeps a single implementation path for backend logic instead of parallel legacy modules

## Known Scope

The current "AI" features are analytics- and rule-driven rather than LLM-native. Insights such as anomaly detection, recurring payment detection, summaries, and chat responses are generated from application logic over user transactions.

## Security Checklist

Before sharing or deploying broadly:

- Rotate any database credentials that have been exposed
- Use a strong `SECRET_KEY`
- Keep `.env` files out of version control
- Restrict `CORS_ORIGIN` to the exact frontend origin you use
- Prefer HTTPS-only deployments

## License

MIT
