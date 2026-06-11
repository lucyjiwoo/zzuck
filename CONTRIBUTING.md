# Contributing Guide

## Git Branching Strategy — GitHub Flow

```
main
 └── feature/auth-login
 └── feature/interview-session
 └── fix/answer-evaluation-bug
 └── chore/update-dependencies
```

### Rules

- `main` is always deployable
- Never commit directly to `main`
- One branch per feature or fix — keep branches short-lived
- Open a PR to merge into `main`; delete the branch after merge

### Branch Naming

```
<type>/<short-description>

feature/resume-upload
fix/pgvector-similarity-query
chore/docker-compose-setup
docs/api-reference
```

---

## Commit Message Convention — Conventional Commits

```
<type>(<scope>): <subject>

[optional body]
```

### Types

| Type | When to use |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `chore` | Tooling, config, deps (no production code change) |
| `docs` | Documentation only |
| `refactor` | Code restructure without behavior change |
| `test` | Adding or updating tests |
| `ci` | GitHub Actions / CI pipeline changes |

### Scope (optional)

Use the service the change belongs to: `frontend`, `backend`, `worker`, `infra`

### Examples

```
feat(backend): add adaptive follow-up question generation
fix(frontend): resolve session state reset on page refresh
chore(infra): add ECS task definition for worker service
docs: update local dev setup instructions
```

---

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker + Docker Compose
- AWS CLI (configured)

### Setup

```bash
# Clone and enter repo
git clone <repo-url>
cd careeriq

# Copy env
cp .env.example .env
# Fill in .env values

# Start local services (Postgres, etc.)
docker compose up -d

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Worker
cd worker
pip install -r requirements.txt
python main.py
```

### Ports

| Service | Port |
|---|---|
| Frontend | 3000 |
| Backend API | 8000 |
| PostgreSQL | 5432 |

---

## Pull Request

- Title follows the same Conventional Commits format
- Keep PRs small and focused — one concern per PR
- Self-review before requesting review
