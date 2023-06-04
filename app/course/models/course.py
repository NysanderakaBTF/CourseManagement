from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import relationship

from .enums.couse_block_type import ContentType
from core.db import Base
from core.db.mixins.timestamp import TimestampMixin
from ...users.models.user import User


class Block(Base):
    __tablename__ = 'blocks'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String, nullable=True, default='No title')
    content = Column(String, default='No content')
    type = Column(Enum(ContentType))
    description = Column(String, default='No description')

    section_id = Column(BigInteger, ForeignKey('section.id'), nullable=False)

    section = relationship('Section', back_populates='blocks')

    completed_content_blocks = relationship('CompletedContentBlock', back_populates='content_block')


class Section(Base):
    __tablename__ = 'section'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, default='No description')
    course_id = Column(BigInteger, ForeignKey('course.id'), nullable=False)

    blocks = relationship('Block', back_populates='section')
    course = relationship('Course', back_populates='sections')


class Course(Base, TimestampMixin):
    __tablename__ = 'courses'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False, default='No description')
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    date_start = Column(TIMESTAMP(timezone=True))
    date_end = Column(TIMESTAMP(timezone=True))

    sections = relationship('Section', back_populates='course')
    user = relationship(User, back_populates='courses')

    participants = relationship('StudentCourse', back_populates='course')


class StudentCourse(TimestampMixin, Base):
    __tablename__ = "student_courses"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    completed = Column(Boolean, default=False)

    student = relationship(User, back_populates="courses")
    course = relationship(Course, back_populates="participants")


class CompletedContentBlock(TimestampMixin, Base):
    __tablename__ = "completed_content_blocks"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_block_id = Column(
        Integer, ForeignKey("blocks.id"), nullable=False
    )
    feedback = Column(Text, nullable=True)
    grade = Column(Integer, default=0)

    student = relationship(User, back_populates="student_content_blocks")
    content_block = relationship(
        Block, back_populates="completed_content_blocks"
    )
