from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Environment
    app_env: str = "local"

    # OpenAI
    openai_api_key: str

    # Database
    database_url: str

    # AWS
    aws_endpoint_url: str | None = None
    sqs_queue_url: str | None = None
    s3_bucket_name: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()