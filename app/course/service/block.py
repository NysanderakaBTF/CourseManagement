from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.course.models import Block
from app.course.service.section import CourseSectionService
from core.db import provide_session


class CourseBlockService:

    @classmethod
    async def create_block(cls, **kwargs) -> Block:
        async with provide_session() as session:
            section = await CourseSectionService.get_course_section_by_id(kwargs.get('section_id'), session)
            if not section:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
            block = Block(**kwargs)
            section.blocks.append(block)
            session.add(block)
            await session.commit()
            await session.refresh(block)
            return block

    @classmethod
    async def get_course_block_by_id(cls, block_id: int) -> Block:
        async with provide_session() as session:
            block = await session.execute(select(Block).where(Block.id == block_id))
            if not block:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Block not found")
            return block.scalar()

    @classmethod
    async def update_block(cls, block_id: int, **kwargs) -> Block:
        async with provide_session() as session:
            block = await CourseBlockService.get_course_block_by_id(session, block_id)
            for key, value in kwargs.items():
                setattr(block, key, value)
            await session.commit()
            await session.refresh(block)
            return block

    @classmethod
    async def delete_block(cls, block_id: int) -> Block:
        async with provide_session() as session:
            block = await CourseBlockService.get_course_block_by_id(session, block_id)
            await session.delete(block)
            await session.commit()

