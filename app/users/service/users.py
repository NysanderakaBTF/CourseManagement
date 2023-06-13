from fastapi.exceptions import HTTPException
from sqlalchemy import select, or_, func, and_
from sqlalchemy.orm import joinedload, contains_eager, selectinload, join, load_only

from app.auth.schema import token_schema
from app.course.models import CompletedContentBlock, Course, Section, Block, StudentCourseAssosiation
from app.users.models.user import User
from app.users.schemas.schemas import *
from core.db.db_config import provide_session
from core.utils.password import PasswordHasher
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
            await session.commit()
            return result.scalars().all()

    @staticmethod
    async def get_user(user_id):
        async with provide_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            await session.commit()
            return user

    @staticmethod
    async def create_user(user: UserCreateRequestSchema):
        async with provide_session() as session:
            print(user)
            print(user.password2)
            print(user.password1)
            if user.password1 != user.password2:
                raise HTTPException(status_code=400, detail="Passwords don't match")
            exists = await session.execute(
                select(User).where(or_(User.email == user.email, User.username == user.username)))
            exists = bool(exists.scalar())
            print(exists)
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
            await session.commit()
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
            await session.commit()

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
            await session.commit()
            return token_schema.JWTTokenSchema(
                access_token=TokenHelper.encode(payload={"user_id": user.id}),
                refresh_token=TokenHelper.encode(payload={"sub": "refresh"})
            )

    @classmethod
    async def get_user_grades(cls, user: User, course_id: int):
        async with provide_session() as session:
            result = await session.execute(
                select(CompletedContentBlock)
                .join(CompletedContentBlock.content_block)
                .join(Block.section)
                .join(Section.course)
                .options(
                    joinedload(CompletedContentBlock.content_block),
                )
                .filter(Course.id == course_id)
            )
            return result.scalars().all()

    @classmethod
    async def get_course_stats(cls, user: User):
        async with provide_session() as session:
            query = (
                select(Course,
                       func.avg(CompletedContentBlock.grade).label("avg_grade"),
                       StudentCourseAssosiation
                       )
                .join(StudentCourseAssosiation)
                .join(Section)
                .join(Block)
                .join(CompletedContentBlock)
                .filter(CompletedContentBlock.student_id == user.id)
                .filter(StudentCourseAssosiation.student_id == user.id)
                .options(load_only(StudentCourseAssosiation.completed),
                         load_only(Course.id, Course.title, Course.description), )
                .group_by(Course.id, StudentCourseAssosiation.id)
            )
        result = await session.execute(query)
        ans = []
        for course, avg, assos in result.unique().fetchall():
            ans.append({
                "assosiation": assos,
                "course": course,
                "avg_grade": avg
            })
        return ans

    @classmethod
    async def get_my_courses(cls, user: User):
        query = (select(Course)
                 .join(StudentCourseAssosiation)
                 .filter(StudentCourseAssosiation.student_id == user.id)
                 .group_by(Course.id)
                 )
        async with provide_session() as session:
            result = await session.execute(query)
            return result.scalars().all()
