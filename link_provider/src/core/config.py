import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    project_name: str = Field(env="PROJECT_NAME", default="RDE")
    project_host: str = Field(env="PROJECT_HOST", default="localhost")
    project_port: int = Field(env="PROJECT_PORT", default=8001)

    bet_maker_url: str = Field(env="BET_MAKER_URL")

    db_user: str = Field(env="DB_USER")
    db_name: str = Field(env="DB_NAME")
    db_host: str = Field(env="DB_HOST")
    db_port: str = Field(env="DB_PORT")
    db_password: str = Field(env="DB_PASSWORD")

    echo: bool = Field(env="ECHO")
    log_level: str = Field(env="LOG_LEVEL", default="INFO")

    class Config:
        env_file = ".env"


settings = Settings()
