from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload
from starlette import status

from app.course.models import Block, ContentType, CompletedContentBlock, Course, Section
from app.course.schemas.block import CreateCompletedBlockRequestSchema
from app.course.service.course import CourseService
from app.course.service.section import CourseSectionService
from core.db import provide_session


class CourseBlockService:

    @classmethod
    async def create_block(cls, cid, **kwargs) -> Block:
        async with provide_session() as session:
            section_id = cid
            section = await CourseSectionService.get_course_section_by_id(cid)
            if not section:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
            if kwargs.get('type') not in (ContentType.__dict__['_member_names_']):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid block type")
            block = Block(**kwargs)
            session.add(block)
            await session.commit()
            await session.refresh(block)
        await CourseSectionService.add_block_to_section(section_id, block)
        return block

    @classmethod
    async def get_course_block_by_id(cls, block_id: int) -> Block:
        async with provide_session() as session:
            block = await session.execute(select(Block).where(Block.id == block_id))
            if not block:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Block not found")
            return block.scalar()

    @classmethod
    async def get_course_blocks_by_section_id(cls, section_id: int) -> list[Block]:
        async with provide_session() as session:
            result = await session.execute(select(Block).where(Block.section_id == section_id))
            return result.scalars().all()

    @classmethod
    async def update_block(cls, block_id: int, **kwargs) -> Block:
        async with provide_session() as session:
            block = await CourseBlockService.get_course_block_by_id(block_id)
            for key, value in kwargs.items():
                if key != "id":
                    setattr(block, key, value)
            session.add(block)
            await session.commit()
        return await cls.get_course_block_by_id(block_id)

    @classmethod
    async def delete_block(cls, block_id: int) -> Block:
        async with provide_session() as session:
            block = await CourseBlockService.get_course_block_by_id(block_id)
            await session.delete(block)
            await session.commit()

    @classmethod
    async def get_block_grade_info_for_user(cls, student_id: int,
                                            block_id: int,
                                            completed_block_id: int = None
                                            ) -> CompletedContentBlock:
        async with provide_session() as session:
            if completed_block_id is None:
                completed_block = await session.execute(
                    select(CompletedContentBlock)
                    .where(and_(CompletedContentBlock.student_id == student_id,
                                CompletedContentBlock.content_block_id == block_id))
                )
                completed_block = completed_block.scalar()
                if not completed_block:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="Mark not found")
                return completed_block

    @classmethod
    async def set_block_mark(cls, course_id: int,
                             rate: CreateCompletedBlockRequestSchema
                             ) -> CompletedContentBlock:
        async with provide_session() as session:
            course = await CourseService.get_course_by_id(course_id)
            if rate.student_id not in [p.id for p in course.participants]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Student is not a course participant")
            print(course.sections.__dict__)
            if rate.content_block_id not in [q.id for p in course.sections for q in p.blocks]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Block is not a course block")
            try:
                block = await cls.get_block_grade_info_for_user(student_id=rate.student_id,
                                                                block_id=rate.content_block_id)
            except HTTPException as e:
                if e.status_code != status.HTTP_404_NOT_FOUND:
                    raise e
                else:
                    block = CompletedContentBlock()
            for key, value in rate.dict().items():
                if key != "id":
                    setattr(block, key, value)
            session.add(block)
            await session.commit()
        # refresh causes error with persisrance
        # async with provide_session() as session:
        #     await session.flush()
        #     await session.refresh(completed)
        return await cls.get_block_grade_info_for_user(student_id=rate.student_id,
                                                       block_id=rate.content_block_id)
