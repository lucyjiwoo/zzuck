# zzuck — AI-Powered SWE Mock Interview Platform

An AI-powered software engineering mock interview platform that conducts adaptive interviews, evaluates answers, and delivers personalized feedback using RAG and OpenAI models.

## System Flow

```
User
 ↓
Frontend (React)
 ↓
FastAPI Backend  ──→  PostgreSQL (job status)
 ↓
SQS Queue
 ↓
Worker Pool on ECS Fargate
 ↓
Evaluation Pipeline
  1. Resume parsing
  2. Job description / target role analysis
  3. Question generation
  4. Answer scoring
  5. Feedback generation
  6. Embedding storage
 ↓
PostgreSQL + pgvector  ←→  S3 (transcripts / reports)
 ↓
Result API
 ↓
Frontend (polling or WebSocket)
```

## Architecture

| Layer | Stack |
|---|---|
| Frontend | React, TypeScript, Vite → Vercel |
| Backend | FastAPI, Python → AWS ECS Fargate |
| Worker | Python SQS consumer → AWS ECS Fargate |
| Database | PostgreSQL + pgvector (AWS RDS) |
| Storage | AWS S3 |
| Queue | AWS SQS |
| Infrastructure | AWS CDK (Python) |
| CI/CD | GitHub Actions |

## Language Strategy

- **Primary**: Python — backend, worker, evaluation pipeline, infra
- **Optional C++**: one high-performance module (e.g. embedding similarity search or answer scoring hot path) integrated via Python bindings

## Key Features

| Feature | Description |
|---|---|
| Job status tracking | `PENDING → PROCESSING → COMPLETED → FAILED` lifecycle per interview job |
| Retry + DLQ | Handles OpenAI API failures, timeouts, and rate limits with SQS retry + dead-letter queue |
| Worker idempotency | Same job processed twice produces the same result without corruption |
| RAG personalization | Previous answers, resume, and target role stored in pgvector for personalized feedback |
| Observability | CloudWatch metrics: queue depth, failure rate, average evaluation latency |

## Repository Structure

```
zzuck/
├── frontend/        # React + TypeScript app
├── backend/         # FastAPI REST API
├── worker/          # Async SQS evaluation worker
├── infra/           # AWS CDK infrastructure (Python)
└── .github/
    └── workflows/   # CI pipelines
```

## Services

- **[frontend](./frontend/README.md)** — User-facing interview UI
- **[backend](./backend/README.md)** — REST API, job dispatch, result delivery
- **[worker](./worker/README.md)** — Evaluation pipeline running on ECS Fargate
- **[infra](./infra/README.md)** — AWS CDK stack and deployment

## CI

| Workflow | Trigger | Jobs |
|---|---|---|
| `frontend-ci` | `frontend/**` | lint, build |
| `backend-ci` | `backend/**`, `worker/**` | pytest (backend + worker) |
| `infra-ci` | `infra/**` | cdk synth |

## Getting Started

1. Clone the repo
2. Copy `.env.example` → `.env` in each service directory and fill in credentials
3. See the README in each subdirectory for service-specific setup
