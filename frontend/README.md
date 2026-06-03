# Frontend

React + TypeScript SPA for the zzuck mock interview platform. Handles the full interview session UX — resume upload, live questioning, and result display. Deployed to Vercel on push to `main`.

## Stack

| | |
|---|---|
| Framework | React 19 |
| Language | TypeScript |
| Bundler | Vite |
| Linting | ESLint |
| Deployment | Vercel |

## Role in the System

- Submits resume and target role to the backend to initiate an interview job
- Displays AI-generated questions one at a time and collects answers
- Polls the Result API (or connects via WebSocket) to display evaluation feedback once the worker pipeline completes
- Shows session history and performance dashboards

## Local Development

```bash
cp .env.example .env
npm install
npm run dev        # http://localhost:3000
```

## Environment Variables

| Variable | Description |
|---|---|
| `VITE_API_BASE_URL` | Backend API base URL |
| `VITE_AUTH_REDIRECT_URL` | OAuth callback URL |

See [.env.example](./.env.example).

## Scripts

| Command | Description |
|---|---|
| `npm run dev` | Start dev server |
| `npm run build` | Type-check + production build |
| `npm run lint` | Run ESLint |
| `npm run preview` | Preview production build locally |

## Deployment

Vercel auto-deploys on push to `main`. Set environment variables in the Vercel project settings.
