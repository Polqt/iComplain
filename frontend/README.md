# iComplain Frontend

SvelteKit frontend for the iComplain campus facility reporting system.

## Stack

- SvelteKit 2 + Svelte 5
- TailwindCSS 4 + DaisyUI 5
- Vitest + Playwright
- Storybook 10
- Optional Tauri desktop shell

## Prerequisites

- Node.js 20+
- npm 10+

## Environment

Create `.env.local` (or use `.env.example`) and configure:

- `PUBLIC_API_URL` (Django API base URL or origin)
- `PUBLIC_GOOGLE_CLIENT_ID` (Google OAuth client id)

Examples:

```env
PUBLIC_API_URL=http://localhost:8000/api
PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

## Commands

```bash
npm install
npm run dev
npm run check
npm run test:unit -- --run
npm run test:e2e
npm run build
npm run preview
```

## Auth Model

This project is sign-in only.

- No self-registration flow
- Users authenticate via school-managed login (Google edu account)
- Session state is managed by Django backend cookies + CSRF

## Project Layout

- `src/routes`: route pages/layouts
- `src/components`: reusable UI
- `src/stores`: application state stores
- `src/lib/api`: typed API clients
- `src/utils`: shared helpers
- `src/stories`: Storybook stories (non-production)

## Notes

- Storybook files are isolated under `src/stories`.
- `src/lib/api/core.ts` provides shared API response/error normalization.
