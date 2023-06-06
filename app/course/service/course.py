from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


from app.course.models.course import Course
from app.users.models import Role
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
                                           .options(selectinload(Course.user),
                                                    selectinload(Course.participants),
                                                    selectinload(Course.sections)
                                                    )
                                           )
            return result.scalars().all()

    @classmethod
    async def get_course_by_id(cls,
                               course_id: int
                               ) -> Course:
        async with provide_session() as session:
            result = await session.execute(select(Course)
                                           .where(Course.id == course_id)
                                           .options(selectinload(Course.user),
                                                    selectinload(Course.participants),
                                                    selectinload(Course.sections)
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
            session.add(instance=course)
            await session.commit()
            await session.refresh(course)
            return course

    @classmethod
    async def update_course(cls, user, course_id, **kwargs) -> Course:
        async with provide_session() as session:
            course = await cls.get_course_by_id(course_id=course_id)
            if course.user.id != user.id:
                raise HTTPException(status_code=403, detail="You are not allowed to update this course")
            course.update(**kwargs)
            await session.commit()
            await session.refresh(course)
            return course

    @classmethod
    async def add_participant_to_course(cls, user, course_id) -> Course:
        async with provide_session() as session:
            course = await cls.get_course_by_id(course_id=course_id)
            course.participants.append(user)
            await session.commit()
            await session.refresh(course)
            return course

    @classmethod
    async def remove_participant_from_course(cls, user, course_id) -> Course:
        async with provide_session() as session:
            course = await cls.get_course_by_id(course_id=course_id)
            course.participants.remove(user)
            await session.commit()
            await session.refresh(course)
            return course

    @classmethod
    async def add_section_to_course(cls, user, course_id, section) -> Course:
        async with provide_session() as session:
            course = await cls.get_course_by_id(course_id=course_id)
            if course.user.id != user.id:
                raise HTTPException(status_code=403, detail="You are not allowed to update this course")
            course.sections.append(section)
            await session.commit()
            await session.refresh(course)
            return course

    @classmethod
    async def delete_course(cls, user, course_id) -> None:
        async with provide_session() as session:
            course = await cls.get_course_by_id(course_id=course_id)
            if course.user.id != user.id:
                raise HTTPException(status_code=403, detail="You are not allowed to delete this course")
            await session.delete(course)
            await session.commit()
