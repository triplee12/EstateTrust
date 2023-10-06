#!/usr/bin/python3
"""Base settings for EstateTrust."""

from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for environment variables."""

    OAUTH2_SECRET_KEY: str
    DB_USER_PASSW: str
    DB_NAME: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_WEEKS: int
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: EmailStr
    ENVIRONMENT: str
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_BUCKET_NAME: str

    class Config:
        """Configuration for environment variables."""

        env_file: str = "./.env"


settings = Settings()
