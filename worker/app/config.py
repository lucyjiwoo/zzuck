from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # local | prod
    app_env: str = "local"

    openai_api_key: str = ""

    # Single connection string — covers host, port, db, user, password
    database_url: str = "postgresql://careeriq:careeriq@localhost:5432/careeriq"

    aws_region: str = "us-east-1"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""

    # Local: http://localhost:4566 (LocalStack)
    # AWS:   leave empty — boto3 uses real AWS endpoints
    aws_endpoint_url: str = ""

    s3_bucket_name: str = ""

    # Queue name — stable identifier independent of the full URL
    queue_name: str = "careeriq-jobs"
    # Full URL — set explicitly so CDK URL changes don't require code changes
    sqs_queue_url: str = ""

    poll_interval_seconds: int = 5

    @property
    def is_local(self) -> bool:
        return self.app_env == "local"

    @property
    def is_prod(self) -> bool:
        return self.app_env == "prod"


settings = Settings()
