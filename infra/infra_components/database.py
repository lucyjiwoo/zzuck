from constructs import Construct


class DatabaseConstruct(Construct):
    """
    RDS PostgreSQL instance with pgvector extension for semantic search.

    Excluded from Phase 2 — added once the data model is finalized to avoid
    paying for an idle RDS instance during early development.

    Planned resources:
    - RDS PostgreSQL 16 instance (t3.micro) in private isolated subnet
    - Auto-generated admin secret via Secrets Manager
    - Security group allowing inbound 5432 from ECS tasks only
    - Deletion protection + final snapshot on removal
    - pgvector extension enabled for embedding storage
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # TODO Phase 3+: implement RDS instance
        # self.instance = rds.DatabaseInstance(self, "Database", ...)
        # self.secret = self.instance.secret
