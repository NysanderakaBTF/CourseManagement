import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload, load_only, subqueryload, joinedload

from app.course.models.course import Course, StudentCourseAssosiation, Section
from app.users.models import Role, User
from core.db.db_config import provide_session


class CourseService:

    def __init__(self):
        pass

    @classmethod
    async def get_courses_list(cls,
                               limit=20,
                               offset=0
                               ) -> List[Course]:
        async with provide_session() as session:
            result = await session.execute(select(Course)
                                           .offset(offset)
                                           .limit(limit)
                                           .options(selectinload(Course.user))
                                           )
            return result.scalars().all()

    @classmethod
    async def get_course_by_id(cls,
                               course_id: int
                               ) -> Course:
        async with provide_session() as session:
            result = await session.execute(select(Course)
                                           .options(joinedload(Course.user),
                                                    joinedload(Course.participants),
                                                    joinedload(Course.sections).joinedload(Section.blocks)
                                                    )
                                           .where(Course.id == course_id)
                                           )
            couse = result.scalar()
            if not couse:
                raise HTTPException(status_code=404, detail="Course not found")
            return couse

    async def get_course_blocks(self, course_id: int) -> Course:
        async with provide_session() as session:
            result = await session.execute(select(Course)
                                           .where(Course.id == course_id)
                                           .options(joinedload(Course.user),
                                                    joinedload(Course.participants),
                                                    joinedload(Course.sections)
                                                    )
                                           )
            couse = result.scalar()
            if not couse:
                raise HTTPException(status_code=404, detail="Course not found")
            return couse

    @classmethod
    async def create_course(cls, user, **kwargs) -> Course:
        async with provide_session() as session:
            course = Course(**kwargs)
            if user.role != Role.teacher:
                raise HTTPException(status_code=403, detail="You are not allowed to create a course")
            course.user = user
            session.add(course)
            await session.commit()
            await session.refresh(course)
            return course

    @classmethod
    async def update_course(cls, user, course_id, **kwargs) -> Course:
        async with provide_session() as session:
            course = await cls.get_course_by_id(course_id=course_id)
            if course.user.id != user.id:
                raise HTTPException(status_code=403, detail="You are not allowed to update this course")
            for key, value in kwargs.items():
                if value:
                    setattr(course, key, value)
            session.add(course)
            await session.commit()
        return await cls.get_course_by_id(course_id=course_id)

    @classmethod
    async def add_participant_to_course(cls, user, course_id) -> Course:
        async with provide_session() as session:
            course = await cls.get_course_by_id(course_id=course_id)
            if user.id not in [i.id for i in course.participants]:
                course.participants.append(user)
                session.add(course)
                await session.commit()
        course = await cls.get_course_by_id(course_id=course_id)
        return course

    @classmethod
    async def remove_participant_from_course(cls, user, course_id) -> Course:
        async with provide_session() as session:
            course = await cls.get_course_by_id(course_id=course_id)
            print(course.participants)
            if user.id in [i.id for i in course.participants]:
                course.participants = [p for p in course.participants if p.id != user.id]
                session.add(course)
                await session.commit()
        course = await cls.get_course_by_id(course_id=course_id)
        return course

    @classmethod
    async def add_section_to_course(cls, user, course_id, section) -> Course:
        async with provide_session() as session:
            course = await cls.get_course_by_id(course_id=course_id)
            if course.user.id != user.id:
                raise HTTPException(status_code=403, detail="You are not allowed to update this course")
            course.sections.append(section)
            await session.flush()
        course = await cls.get_course_by_id(course_id=course_id)
        return course

    @classmethod
    async def delete_course(cls, user, course_id) -> None:
        async with provide_session() as session:
            course = await cls.get_course_by_id(course_id=course_id)
            if course.user.id != user.id:
                raise HTTPException(status_code=403, detail="You are not allowed to delete this course")
            await session.delete(course)
            await session.commit()

    @classmethod
    async def get_new_courses(cls, days):
        start_date = datetime.datetime.utcnow() - datetime.timedelta(days=days)
        end_date = datetime.datetime.utcnow()

        stmt = select(Course).where(
            and_(
                Course.created_at >= start_date,
                Course.created_at <= end_date
            )
        )
        async with provide_session() as session:
            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def get_updated_courses(cls, days):
        start_date = datetime.datetime.utcnow() - datetime.timedelta(days=days)
        end_date = datetime.datetime.utcnow()

        stmt = select(Course).where(
            and_(
                Course.updated_at >= start_date,
                Course.updated_at <= end_date
            )
        )
        async with provide_session() as session:
            result = await session.execute(stmt)
            return result.scalars().all()
