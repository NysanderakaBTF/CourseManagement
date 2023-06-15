import os

from pydantic import BaseSettings, PostgresDsn


class Config(BaseSettings):
    DB_URL: PostgresDsn
    JWT_SECRET_KEY: str = f"{os.getenv('JWT_SECRET_KEY')}"
    JWT_ALGORITHM: str = f"{os.getenv('JWT_ALGORITHM')}"
    EMAIL_HOST: str = f"{os.getenv('EMAIL_HOST')}"
    EMAIL_HOST_USER: str = f"{os.getenv('EMAIL_HOST_USER')}"
    EMAIL_HOST_PASSWORD: str = f"{os.getenv('EMAIL_HOST_PASSWORD')}"
    EMAIL_PORT: str = f"{os.getenv('EMAIL_PORT')}"
    CELERY_BROKER_URL: str = f"{os.getenv('CELERY_BROKER_URL')}"
    CELERY_BACKEND_URL: str = f"{os.getenv('CELERY_BACKEND_URL')}"


config = Config()
