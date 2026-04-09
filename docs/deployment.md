# Deployment Guide

## Current Production Auth Issues

The current production sign-in problems shown in the screenshots map to two separate deployment issues:

1. `Failed to fetch` on email/password sign-in:
   Django is rejecting the Vercel frontend origin during the CSRF bootstrap request because the production frontend origin is not included in backend CORS/CSRF configuration.

2. `Error 400: origin_mismatch` on Google sign-in:
   The Google OAuth client does not list the deployed frontend origin in its Authorized JavaScript origins.

## Architecture

- Frontend: Vercel
- Backend API + WebSocket server: Render
- Database: Neon Postgres
- Cache / Channels / Celery broker: optional Redis
- Desktop app: Tauri, with the frontend bundled into the app

## Required Frontend Variables

Set these in Vercel for Production:

```env
PUBLIC_API_URL=https://icomplain-backend.onrender.com/api
PUBLIC_GOOGLE_CLIENT_ID=your-google-web-client-id.apps.googleusercontent.com
```

Notes:

- `PUBLIC_API_URL` should point to the Render backend `/api` base.
- `PUBLIC_GOOGLE_CLIENT_ID` must match the backend `GOOGLE_OAUTH2_CLIENT_ID`.

## Required Backend Variables

Set these in Render for Production:

```env
SECRET_KEY=change-me
DEBUG=False
ALLOWED_HOSTS=icomplain-backend.onrender.com
FRONTEND_URL=https://i-complain.vercel.app
CORS_ALLOWED_ORIGINS=https://i-complain.vercel.app,http://localhost:5173,http://127.0.0.1:5173,https://tauri.localhost,tauri://localhost
GOOGLE_OAUTH2_CLIENT_ID=your-google-web-client-id.apps.googleusercontent.com
ALLOWED_EMAIL_DOMAINS=usls.edu.ph
DATABASE_URL=postgresql://.../dbname?sslmode=require
REDIS_URL=
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
DEFAULT_FROM_EMAIL=...
SEED_ADMIN_EMAIL=usls.admin@usls.edu.ph
SEED_ADMIN_PASSWORD=your-strong-password
SEED_ADMIN_FULL_NAME=USLS Admin
```

If you also want auth to work on Vercel preview deployments, add each preview origin explicitly to `CORS_ALLOWED_ORIGINS` while testing.

## Google OAuth Setup

Create or edit a Google OAuth 2.0 **Web application** client and add these Authorized JavaScript origins:

- `https://i-complain.vercel.app`
- `http://localhost:5173`
- `http://127.0.0.1:5173`

If you use a Vercel preview URL for testing Google sign-in, add that exact preview URL too.

Then copy the same client ID into:

- Vercel: `PUBLIC_GOOGLE_CLIENT_ID`
- Render: `GOOGLE_OAUTH2_CLIENT_ID`

## CI/CD Flow

This repo now uses GitHub Actions for CI and relies on the existing GitHub integrations on Vercel and Render for CD.

- Push or merge to `main`
- GitHub Actions runs frontend and backend checks
- Vercel deploys the frontend from the connected GitHub repo
- Render deploys the backend from the connected GitHub repo

Recommended platform settings:

- Vercel:
  - Root directory: `frontend`
  - Build command: `npm run build`
  - Output directory: `build`
- Render:
  - Root directory: `backend`
  - Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
  - Start command: `python scripts/predeploy_migrate.py && python scripts/start_server.py`

## Release Tags

Create an annotated release tag after `main` is in a deployable state:

```bash
git checkout main
git pull origin main
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

Then create the GitHub Release from that tag in the repository Releases page.

Suggested versioning:

- `v0.1.0` for first stable release
- `v0.1.1` for fixes
- `v0.2.0` for new features
- `v1.0.0` when you consider the product production-ready

## Tauri Desktop Build

Development:

```bash
cd frontend
npm install
npm run tauri:dev
```

Production desktop bundle:

```bash
cd frontend
npm install
npm run tauri:build
```

Important behavior:

- In `tauri:dev`, Tauri uses the local Vite dev server from `http://localhost:5173`.
- In `tauri:build`, the frontend is bundled into the desktop app, so you do **not** need to run a local frontend server.
- The desktop app will still need a backend API. If `PUBLIC_API_URL` points to Render at build time, the packaged desktop app talks to Render directly and does **not** need `python manage.py runserver`.

## Production Deployment Checklist

1. Set the Render backend env vars from `backend/.env.example`.
2. Set the Vercel frontend env vars from `frontend/.env.example`.
3. Add the Vercel production origin to Google OAuth Authorized JavaScript origins.
4. Redeploy Render.
5. Redeploy Vercel.
6. Test `/signin` again with both email/password and Google sign-in.
