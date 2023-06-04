from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import async_scoped_session

from app.users.models.user import User
from core.db.db_config import get_async_session
from app.users.schemas.schemas import  *
from core.utils.password import PasswordHasher
from app.auth.schema import token_schema
from core.utils.token import TokenHelper


class UserService:
    def __init__(self):
        pass

    async def get_all_users(self,
                            session=Annotated[async_scoped_session, Depends(get_async_session)],
                            limit: int = 10,
                            offset: int = 0
                            ):
        result = await session.execute(select(User).limit(limit).offset(offset).all())
        return result.scalars().all()

    async def get_user(self,
                       user_id,
                       session=Annotated[async_scoped_session, Depends(get_async_session)]):
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def create_user(self, user: UserCreateRequestSchema, session=Annotated[async_scoped_session, Depends(get_async_session)]):
        if user.password1 != user.password2:
            raise HTTPException(status_code=400, detail="Passwords don't match")
        exists = await session.execute(select(User).where(or_(User.email == user.email, User.username == user.username)).exists())
        if exists:
            raise HTTPException(status_code=400, detail="Username or email already exists")
        data = user.dict()
        data['password'] = PasswordHasher.hash(data['password1'])
        data.pop('password1')
        data.pop('password2')
        user = User(**data)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def update_user(self, user):
        pass

    async def delete_user(self, user_id):
        pass

    async def authenticate_user(self,
                                username: str,
                                password: str,
                                session=Annotated[async_scoped_session, Depends(get_async_session)]):
        res = await session.execute(select(User).where(User.username == username))
        user = res.scalar()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not PasswordHasher.verify(password, user.password):
            raise HTTPException(status_code=401, detail="Incorrect password")

        return token_schema.JWTTokenSchema(
            token=TokenHelper.encode(payload={"user_id": user.id}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"})
        )



