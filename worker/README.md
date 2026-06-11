# Worker

Async Python worker pool running on AWS ECS Fargate. Consumes interview evaluation jobs from SQS and runs a multi-step AI pipeline to produce scored, personalized feedback.

## Stack

| | |
|---|---|
| Language | Python 3.11 (+ optional C++ module for hot path) |
| Config | pydantic-settings |
| Queue | AWS SQS (consumer) |
| AI | OpenAI GPT & Embedding models |
| Database | PostgreSQL + pgvector (AWS RDS) |
| Storage | AWS S3 |
| Deployment | AWS ECS Fargate |

## Evaluation Pipeline

Each job consumed from SQS runs through the following steps in order:

1. **Resume parsing** — extract structured experience and skills from the uploaded resume
2. **Job description / target role analysis** — identify required competencies and seniority signals
3. **Question generation** — produce adaptive interview questions tailored to the candidate's profile
4. **Answer scoring** — evaluate the candidate's answer against expected signals
5. **Feedback generation** — produce actionable, personalized written feedback via GPT
6. **Embedding storage** — store answer embeddings in pgvector for RAG-based personalization in future sessions

## Reliability Design

| Concern | Approach |
|---|---|
| Job status | Updates PostgreSQL record: `PENDING → PROCESSING → COMPLETED → FAILED` |
| Retry + DLQ | SQS retries up to 3 times on failure; dead-letter queue captures persistent failures |
| Idempotency | Each job is keyed by a stable job ID — reprocessing produces the same result |
| RAG personalization | Previous answers, resume, and target role retrieved from pgvector to personalize feedback |
| Observability | CloudWatch metrics: queue depth, failure rate, average evaluation latency per step |

## How It Works

1. `poll()` long-polls SQS for messages
2. Each message is dispatched to a handler by `type` field
3. Handler updates job status in PostgreSQL before and after processing
4. On unhandled exception, the message visibility timeout expires and SQS retries
5. After 3 failures, the message moves to the DLQ
6. Graceful shutdown on `SIGTERM` / `SIGINT` for ECS task draining

## Local Development

```bash
cd worker
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env        # fill in credentials
python -m app.main
```

## Environment Variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key |
| `POSTGRES_HOST` | Database host |
| `POSTGRES_PORT` | Database port (default: `5432`) |
| `POSTGRES_DB` | Database name (default: `careeriq`) |
| `POSTGRES_USER` | Database user |
| `POSTGRES_PASSWORD` | Database password |
| `AWS_REGION` | AWS region (default: `us-east-1`) |
| `AWS_ACCESS_KEY_ID` | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key |
| `S3_BUCKET_NAME` | S3 bucket for transcripts / reports |
| `SQS_QUEUE_URL` | SQS queue URL to consume from |
| `POLL_INTERVAL_SECONDS` | Polling interval in seconds (default: `5`) |

See [.env.example](./.env.example).

## Running Tests

```bash
pytest
```

## Adding a New Job Type

1. Add a handler function in `app/handlers/`
2. Register the message `type` → handler mapping in `app/handlers/handler_log.py`
