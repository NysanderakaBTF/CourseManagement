from typing import List, Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_scoped_session

from app.course.models.course import Course
from core.db.db_config import get_async_session


class CourseService:

    def __init__(self):
        pass

    @classmethod
    async def get_courses_list(cls,
                               limit=20,
                               offset=0,
                               session=Annotated[async_scoped_session, Depends(get_async_session)]
                               ) -> List[Course]:
        result = await session.execute(select(Course).offset(offset).limit(limit))
        print(result.scalars().all())
        return result

    @classmethod
    async def get_course_by_id(cls,
                               course_id: int,
                               session=Annotated[async_scoped_session, Depends(get_async_session)]) -> List[Course]:
        result = await session.execute(select(Course).where(Course.id == course_id))
        couse = result.scalar()
        if not couse:
            raise HTTPException(status_code=404, detail="Course not found")
        return couse

    @classmethod
    async def create_course(cls, session=Annotated[async_scoped_session, Depends(get_async_session)],  **kwargs):
        course = Course(**kwargs)
        session.add(course)
        await session.commit()
        await session.refresh(course)
        return course