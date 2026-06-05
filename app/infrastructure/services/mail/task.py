from dataclasses import dataclass
from email.message import EmailMessage

import aiosmtplib
from dishka import FromDishka
from dishka.integrations.taskiq import inject

from app.application.interfaces.queue import BaseTask
from app.configs.app import app_config
from app.configs.smtp import SMTPConfig



@dataclass
class SendEmail(BaseTask):
    __task_name__ = "mail.send"

    @staticmethod
    @inject
    async def run(content: str, email_data: dict, smtp_config: FromDishka[SMTPConfig]) -> None:
        sender_name = email_data["sender_name"] or app_config.EMAIL_SENDER_NAME
        sender_address = email_data["sender_address"] or app_config.EMAIL_SENDER_ADDRESS

        message = EmailMessage()
        message["From"] = f"{sender_name} <{sender_address}>"
        message["To"] = email_data["recipient"]
        message["Subject"] = f"{app_config.PROJECT_NAME} | {email_data['subject']}"
        message.add_alternative(content, subtype="html")

        await aiosmtplib.send(message, **smtp_config)
