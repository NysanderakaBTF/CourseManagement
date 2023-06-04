import os

from pydantic import BaseSettings


class Config(BaseSettings):
    # DB_URL: str = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER_DEV')}:" \
    #                      f"{os.getenv('POSTGRES_PASSWORD_DEV')}@" \
    #                      f"{os.getenv('POSTGRES_HOST_DEV')}:" \
    #                      f"{os.getenv('POSTGRES_PORT_DEV')}/{os.getenv('POSTGRES_DB_DEV')}"
    DB_URL: str = f"postgresql+asyncpg://Fox:" \
                         f"123@" \
                         f"localhost:" \
                         f"5432/course"
    JWT_SECRET_KEY: str = "2b6a9e4fac2215f8f0c7d689667cb2afd60cdc9d88c487d35b7beb894b88fd14"
    JWT_ALGORITHM: str = "HS256"

config = Config()