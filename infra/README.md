# Infra

AWS CDK (Python) project that defines all cloud infrastructure for Career IQ. Resources are organized into focused constructs under `infra_components/` and assembled in `stacks/core_infra_stack.py`.

## Stack

| | |
|---|---|
| IaC Tool | AWS CDK v2 |
| Language | Python 3.11 |
| Deployment | `cdk deploy` |

## Project Structure

```
infra/
├── app.py                        # CDK app entrypoint
├── stacks/
│   └── core_infra_stack.py       # CareerIQStack — assembles all constructs
└── infra_components/
    ├── networking.py             # VPC, subnets
    ├── compute.py                # ECR, ECS cluster, task definitions, CloudWatch
    ├── storage.py                # S3 (planned)
    ├── database.py               # RDS PostgreSQL + pgvector (planned)
    └── messaging.py              # SQS + DLQ (planned)
```

## Resources by Phase

### Phase 2 — Current

| Resource | Details |
|---|---|
| **VPC** | 2 AZs, public + private isolated subnets, no NAT gateway |
| **ECR** | `careeriq-backend` repository (5-image lifecycle) |
| **ECS Cluster** | Fargate cluster (`careeriq`) with Container Insights |
| **ECS Task Def** | Backend task definition (port 8000) |
| **CloudWatch** | Log group `/ecs/careeriq-backend`, 1-week retention |

### Phase 3+ — Planned

| Resource | Details |
|---|---|
| **NAT Gateway** | Enables private subnet outbound internet access |
| **RDS** | PostgreSQL 16, private subnet, pgvector extension, auto-rotated secret |
| **SQS** | `careeriq-jobs` queue + DLQ (3 retries, 14-day retention) |
| **S3** | Private bucket for resumes, transcripts, and evaluation reports |
| **Worker Task Def** | ECS task definition for the worker pool |
| **Fargate Services** | Backend + worker services with auto-scaling |

## Local Setup

```bash
cd infra
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
npm install -g aws-cdk

cp .env.example .env        # fill in AWS credentials
```

## Environment Variables

| Variable | Description |
|---|---|
| `AWS_REGION` | Target AWS region (default: `us-east-1`) |
| `AWS_ACCESS_KEY_ID` | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key |

See [.env.example](./.env.example).

## Common Commands

| Command | Description |
|---|---|
| `cdk synth` | Synthesize CloudFormation template |
| `cdk diff` | Show changes vs deployed stack |
| `cdk deploy` | Deploy stack to AWS |
| `cdk destroy` | Tear down all resources |

## Stack Outputs

| Output | Description |
|---|---|
| `BackendRepoUri` | ECR URI for the backend image |
| `EcsClusterName` | ECS cluster name |
| `BackendLogGroupName` | CloudWatch log group for the backend service |
