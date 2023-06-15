import asyncio

from app.course.service.course import CourseService
from app.users.service.users import UserService
from core.utils.email import EmailService
from . import celery_app


@celery_app.task(name='send_new_courses')
def send_new_courses():
    courses = asyncio.run(CourseService.get_new_courses(7))
    users = asyncio.run(UserService.get_all_users())
    print("!!!!!!!!!!!!!!!!!!!!!!")

    asyncio.run(await EmailService.send_email(
        [user.email for user in users],
        'New Courses',
        courses
    ))


@celery_app.task(name='send_updated_courses')
def send_updated_courses():
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    courses = asyncio.run(CourseService.get_updated_courses(7))
    users = asyncio.run(UserService.get_all_users())

    asyncio.run(EmailService.send_email(
        [user.email for user in users],
        'New Courses',
        courses
    ))
