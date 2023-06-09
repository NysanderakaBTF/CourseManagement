import datetime
import http
import smtplib
from datetime import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from typing import List

import aiosmtplib.errors
from aiosmtplib import SMTP
from fastapi import HTTPException

from core.config import config


class EmailService:

    EMAIL_HOST = config.EMAIL_HOST
    EMAIL_PORT = config.EMAIL_PORT
    EMAIL_HOST_USER = config.EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = config.EMAIL_HOST_PASSWORD

    def __init__(self):
        ...

    # async def send_email(self, to, subject, body):
    #     try:
    #         smtp = SMTP(hostname=self.EMAIL_HOST, port=self.EMAIL_PORT)
    #         await smtp.connect()
    #         await smtp.starttls()
    #         await smtp.login(self.EMAIL_HOST_USER, self.EMAIL_HOST_PASSWORD)
    #         await smtp.send_message(
    #             body,
    #             sender=self.EMAIL_HOST_USER,
    #             recipients=self.join_recipients(to),
    #             subject=subject
    #         )
    #         await smtp.quit()
    #     except aiosmtplib.errors.SMTPException as e:
    #         print(e)
    #
    # def join_recipients(self, recipients: str | List[str]) -> str:
    #     if isinstance(recipients, list):
    #         return COMMASPACE.join(recipients)
    #     return recipients


    def send_email(self, to, subject, body):
        try:
            body += '\nTime Sent: ' + str(datetime.datetime.utcnow())
            msg = MIMEMultipart()
            msg['Subject'] = subject
            body = MIMEText(body)
            msg.attach(body)
            msg['To'] = self.join_recipients(to)

            smtp = smtplib.SMTP(self.EMAIL_HOST, self.EMAIL_PORT)
            smtp.starttls()
            smtp.login(self.EMAIL_HOST_USER, self.EMAIL_HOST_PASSWORD)
            smtp.sendmail(
                self.EMAIL_HOST_USER,
                to,
                msg.as_string()
            )
            smtp.quit()
        except Exception as e:
            print(e)

    def join_recipients(self, recipients: str | List[str]) -> str:
        if isinstance(recipients, list):
            return COMMASPACE.join(recipients)
        return recipients
