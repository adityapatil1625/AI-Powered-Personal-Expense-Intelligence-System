# Deployment Guide

This project is set up to run with:

- Frontend on Vercel
- Backend on Render
- Database on Supabase Postgres

## 1. Supabase

Use your existing Supabase Postgres database.

Recommended connection string for Render:

```env
DATABASE_URL=postgresql://postgres.<project-ref>:[YOUR-PASSWORD]@aws-0-<region>.pooler.supabase.com:5432/postgres
```

Notes:

- Supabase recommends a pooler connection for persistent servers when you need broad network compatibility.
- If your direct connection string already works from Render, you can keep using it.

## 2. Backend on Render

The repo includes [`render.yaml`](C:\Users\adity\Desktop\expense-intelligence\render.yaml), so you can create the backend as a Blueprint-backed web service.

Render settings:

- Root directory: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app.main:app`

Required environment variables on Render:

```env
DATABASE_URL=<your-supabase-connection-string>
SECRET_KEY=<long-random-secret>
DEBUG=False
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGIN=https://<your-vercel-app>.vercel.app
CORS_ORIGIN_REGEX=^https?://(localhost|127\\.0\\.0\\.1)(:\\d+)?$|^https://.*\\.vercel\\.app$
```

After deploy, your API base URL will look like:

```text
https://expense-intelligence-api.onrender.com
```

Check:

- `GET /` should return a health response
- `GET /docs` should open FastAPI docs

## 3. Frontend on Vercel

Create a Vercel project from the `frontend` directory.

Recommended Vercel project settings:

- Framework preset: `Vite`
- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`

Required environment variable on Vercel:

```env
VITE_API_URL=https://<your-render-service>.onrender.com
```

The frontend reads this variable at build time, so redeploy Vercel after changing it.

## 4. Connection Flow

Once all three are set:

1. Vercel frontend sends requests to `VITE_API_URL`
2. Render backend connects to Supabase using `DATABASE_URL`
3. Render CORS allows your Vercel production URL and Vercel preview URLs

## 5. Local Development

Backend:

```bash
cd backend
cp .env.example .env
python run.py
```

Frontend:

```bash
cd frontend
cp .env.example .env.local
npm run dev
```

Use:

```env
VITE_API_URL=http://localhost:8000
```

## 6. Important Notes

- The frontend chat request is now aligned with the backend API contract.
- The backend runner now respects `PORT`, which helps on hosted platforms.
- Vercel preview deployments should work because the backend now allows `https://*.vercel.app` through `CORS_ORIGIN_REGEX`.
