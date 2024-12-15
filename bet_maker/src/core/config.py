import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    project_name: str = Field(env="PROJECT_NAME", default="Betting Software (Bet-Maker)")
    project_host: str = Field(env="PROJECT_HOST", default="0.0.0.0")
    project_port: int = Field(env="PROJECT_PORT", default=8000)

    link_provider_url: str = Field(env="LINK_PROVIDER_URL", default="http://localhost:8001")

    db_user: str = Field(env="DB_USER")
    db_name: str = Field(env="DB_NAME")
    db_host: str = Field(env="DB_HOST")
    db_port: str = Field(env="DB_PORT")
    db_password: str = Field(env="DB_PASSWORD")

    redis_host: str = Field(env="REDIS_HOST", default="127.0.0.1")
    redis_port: int = Field(env="REDIS_PORT", default=6379)

    echo: bool = Field(env="ECHO")
    log_level: str = Field(env="LOG_LEVEL", default="INFO")

    class Config:
        env_file = ".env"


settings = Settings()
