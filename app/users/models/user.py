from sqlalchemy import Column, BigInteger, String, Boolean, Enum
from sqlalchemy.orm import relationship

from app.users.models.enums.roles import Role
from core.db.db_config import Base
from core.db.mixins.timestamp import TimestampMixin



class User(Base, TimestampMixin):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    is_admin = Column(Boolean, default=False)
    role = Column(Enum(Role), index=True, nullable=False)

    courses = relationship("StudentCourse", back_populates="student")
    student_content_blocks = relationship(
        "CompletedContentBlock", back_populates="student"
    )
