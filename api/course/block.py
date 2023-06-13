from typing import List

from fastapi import APIRouter

from app.course.schemas.block import CreateCompletedBlockResponseSchema, \
    CreateCourseBlockRequestSchema, \
    RetriveCourseBlockResponseSchema, \
    CreateCourseBlockResponseSchema, \
    CreateCompletedBlockRequestSchema
from app.course.service.block import CourseBlockService

block_router = APIRouter(prefix="/courses/{course_id}/section/{cid}",
                         tags=["block"])


@block_router.get("/blocks",
                  response_model=List[RetriveCourseBlockResponseSchema],
                  description="Getting all course blocks for a section")
async def get_blocks(cid: int):
    return await CourseBlockService.get_course_blocks_by_section_id(cid)


@block_router.post("/blocks",
                   response_model=CreateCourseBlockResponseSchema,
                   description="Creating a new block for a section")
async def create_block(cid: int, block: CreateCourseBlockRequestSchema):
    return await CourseBlockService.create_block(cid=cid, **block.dict())


@block_router.get("/blocks/{bid}",
                  response_model=RetriveCourseBlockResponseSchema,
                  description="Getting a course block by id")
async def get_block(cid: int, bid: int):
    return await CourseBlockService.get_course_block_by_id(bid)


@block_router.put("/blocks/{bid}",
                  response_model=RetriveCourseBlockResponseSchema,
                  description="Updating a course block by id")
async def update_block(cid: int,
                       bid: int,
                       block: RetriveCourseBlockResponseSchema):
    return await CourseBlockService.update_block(bid, **block.dict())


@block_router.delete("/blocks/{bid}",
                     description="Deleting a course block by id")
async def delete_block(cid: int, bid: int):
    return await CourseBlockService.delete_block(bid)


@block_router.put("/blocks/{bid}/mark",
                  description="Setting a course block mark")
async def post_block_mark(course_id: int,
                          mark: CreateCompletedBlockRequestSchema):
    return await CourseBlockService.set_block_mark(course_id=course_id,
                                                   rate=mark)
