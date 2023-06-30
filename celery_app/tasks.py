import asyncio
import json

from app.course.service.course import CourseService
from app.users.service.users import UserService
from core.utils.email import EmailService
from core.utils.sqla_serializer import serialize, datetime_handler
from . import celery_app


@celery_app.task(name='send_new_courses')
def send_new_courses():
    loop = asyncio.get_event_loop()
    res = []
    async def run_and_capture_result():
        r = await CourseService.get_new_courses(7)
        res.append(r)
        r = await UserService.get_all_users()
        res.append(r)
    loop.run_until_complete(run_and_capture_result())
    print("!!!!!!!!!!!!!!!!!!!!!!")
    print(res[1])
    # loop.run_until_complete(EmailService().send_email(
    #     to=[user.email for user in res[1]],
    #     subject='New Courses',
    #     body=('\n'.join([json.dumps(serialize(course), default=datetime_handler) for course in res[0]]))
    # ))
    EmailService().send_email(
        to=[user.email for user in res[1]],
        subject='New Courses',
        body=('\n'.join([json.dumps(serialize(course), default=datetime_handler) for course in res[0]]))
    )


@celery_app.task(name='send_updated_courses')
def send_updated_courses():
    loop = asyncio.get_event_loop()
    res = []

    async def run_and_capture_result():
        r = await CourseService.get_updated_courses(7)
        res.append(r)
        r = await UserService.get_all_users()
        res.append(r)

    loop.run_until_complete(run_and_capture_result())
    print("AAAAAAAAAAAAAAAAAAAAAAA")
    print(res[1])
    print('\n'.join([json.dumps(serialize(course), default=datetime_handler) for course in res[0]]))
    # loop.run_until_complete(EmailService().send_email(
    #     to=[user.email for user in res[1]],
    #     subject='New Courses',
    #     body=('\n'.join([json.dumps(serialize(course), default=datetime_handler) for course in res[0]]))
    # ))
    EmailService().send_email(
        to=[user.email for user in res[1]],
        subject='Updated Courses',
        body=('\n'.join([json.dumps(serialize(course), default=datetime_handler) for course in res[0]]))
    )

