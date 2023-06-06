from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import select, or_

from app.users.models.user import User
from core.db.db_config import provide_session
from app.users.schemas.schemas import  *
from core.utils.password import PasswordHasher
from app.auth.schema import token_schema
from core.utils.token import TokenHelper


class UserService:
    def __init__(self):
        pass
    @staticmethod
    async def get_all_users(limit: int = 10,
                            offset: int = 0
                            ):
        async with provide_session() as session:
            result = await session.execute(select(User).limit(limit).offset(offset).all())
            return result.scalars().all()

    @staticmethod
    async def get_user(user_id):
        async with provide_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user

    @staticmethod
    async def create_user(user: UserCreateRequestSchema):
        async with provide_session() as session:
            if user.password1 != user.password2:
                raise HTTPException(status_code=400, detail="Passwords don't match")
            exists = await session.execute(select(User).where(or_(User.email == user.email, User.username == user.username)))
            exists = exists.scalar()
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

    @staticmethod
    async def update_user(user_upd: RetriveUserResponseSchema):
        async with provide_session() as session:
            user = await session.execute(select(User).where(User.id == user_upd.id))
            user = user.scalar()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            for key, value in user_upd.dict().items():
                setattr(user, key, value)

    @staticmethod
    async def delete_user(current_user: User):
        async with provide_session() as session:
            session.delete(current_user)
            await session.commit()


    @staticmethod
    async def authenticate_user(username: str,
                                password: str,
                               ):
        async with provide_session() as session:
            res = await session.execute(select(User).where(User.username == username))
            user = res.scalar()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            if not PasswordHasher.verify(password, user.password):
                raise HTTPException(status_code=401, detail="Incorrect password")

            return token_schema.JWTTokenSchema(
                access_token=TokenHelper.encode(payload={"user_id": user.id}),
                refresh_token=TokenHelper.encode(payload={"sub": "refresh"})
            )



