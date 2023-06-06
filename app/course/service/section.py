from typing import List

from fastapi import HTTPException
from select import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.course.models import Section, Course
from app.course.service.course import CourseService
from app.users.models import User, Role
from core.db import provide_session


class CourseSectionService:
    def __init__(self):
        pass

    @classmethod
    async def get_course_section_by_id(cls,
                                       course_section_id: int,
                                       ) -> Section:
        async with provide_session() as session:
            result = await session.execute(select(Section)
                                           .where(Section.id == course_section_id)
                                           .options(selectinload(Section.blocks)))
            return result.scalar()

    @classmethod
    async def get_course_sections_by_course_id(cls,
                                               course_id: int
                                               ) -> List[Section]:
        async with provide_session() as session:
            result = await session.execute(select(Section)
                                           .where(Section.course_id == course_id)
                                           .options(selectinload(Section.blocks)))
            return result.scalars().all()

    @classmethod
    async def create_course_section(cls, user: User, **kwargs) -> Section:
        async with provide_session() as session:
            course_id = kwargs["course_id"]
            course = await CourseService.get_course_by_id(course_id, session)
            if user.role != Role.teacher or course.user_id != user.id:
                raise HTTPException(status_code=403, detail="You are not allowed to modify this course")
            section = Section(**kwargs)
            session.add(section)
            await session.commit()
            await session.refresh(section)
            await CourseService.add_section_to_course(session, user, course.id, section)
            return section

    @classmethod
    async def delete_course(cls, user: User, section_id: int) -> None:
        async with provide_session() as session:
            section = await session.execute(select(Section)
                                            .join(Section.course)
                                            .where(Section.id == section_id))
            print(section)
            print(section.scalar())
            section = section.scalar()
            if user.role != Role.teacher and section.course.id != user.id:
                raise HTTPException(status_code=403, detail="You are not allowed to modify this course")
            await session.delete(section)
            await session.commit()