import http
from email.mime.multipart import MIMEMultipart
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

    async def send_email(self, to, subject, body):
        try:
            smtp = SMTP(hostname=self.EMAIL_HOST, port=self.EMAIL_PORT)
            await smtp.connect()
            await smtp.starttls()
            await smtp.login(self.EMAIL_HOST_USER, self.EMAIL_HOST_PASSWORD)
            await smtp.send_message(
                body,
                sender=self.EMAIL_HOST_USER,
                recipients=self.join_recipients(to),
                subject=subject
            )
            await smtp.quit()
        except aiosmtplib.errors.SMTPException:
            raise HTTPException(status_code=http.HTTPStatus.SERVICE_UNAVAILABLE, detail="Unable to send email")

    def join_recipients(self, recipients: str | List[str]) -> str:
        if isinstance(recipients, list):
            return COMMASPACE.join(recipients)
        return recipients
