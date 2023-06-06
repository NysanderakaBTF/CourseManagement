from jose import JWTError

from app.auth.schema.token_schema import JWTTokenSchema
from core.utils.token import TokenHelper


class JWTTokenService:
    async def create_access_token(self, data: dict):
        return TokenHelper.encode(payload=data)

    async def create_refresh_token(self, token: str,
                                   refresh_token: str):
        token = TokenHelper.decode(token=token)
        refresh_token = TokenHelper.decode(token=refresh_token)
        if refresh_token.get("sub") != "refresh":
            raise JWTError("Invalid refresh token")
        #TODO: get expiresion time from env
        return JWTTokenSchema(
            token=TokenHelper.encode(payload={"user_id": token.get("user_id")}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )

    async def verify_token(self, token: str):
        return TokenHelper.decode(token=token)
