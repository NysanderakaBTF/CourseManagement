import os

from pydantic import BaseSettings


class Config(BaseSettings):
    # DB_URL: str = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:" \
    #                      f"{os.getenv('POSTGRES_PASSWORD')}@" \
    #                      f"{os.getenv('POSTGRES_HOST')}:" \
    #                      f"{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    DB_URL: str = f"postgresql+asyncpg://postgres:" \
                         f"postgres@" \
                         f"localhost:" \
                         f"5432/course"
    JWT_SECRET_KEY: str = f"{os.getenv('JWT_SECRET_KEY')}"
    JWT_ALGORITHM: str = f"{os.getenv('JWT_ALGORITHM')}"

config = Config()