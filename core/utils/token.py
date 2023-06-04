from datetime import datetime, timedelta

from jose import jwt, JWTError

from core.config import config


class TokenHelper:
    @staticmethod
    def encode(payload: dict, expire_period: int = 3600) -> str:
        token = jwt.encode(
            {
                **payload,
                "exp": datetime.utcnow() + timedelta(seconds=expire_period),
            },
            key=config.JWT_SECRET_KEY,
            algorithm=config.JWT_ALGORITHM,
        )
        return token

    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                config.JWT_SECRET_KEY,
                config.JWT_ALGORITHM,
            )
        except jwt.JWTError:
            raise jwt.JWTError
