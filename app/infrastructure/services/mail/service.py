from dataclasses import dataclass
from email.message import EmailMessage

import aiosmtplib

from app.application.interfaces.mail import BaseMailService, BaseTemplate, EmailData
from app.application.interfaces.queue import QueueService
from app.configs.app import app_config
from app.configs.smtp import SMTPConfig
from app.infrastructure.services.mail.task import SendEmail



@dataclass
class AioSmtpLibMailService(BaseMailService):
    smtp_config: SMTPConfig
    queue_service: QueueService

    async def send(self, template: BaseTemplate, email_data: EmailData) -> None:
        sender_name = email_data.sender_name or app_config.EMAIL_SENDER_NAME
        sender_address = email_data.sender_address or app_config.EMAIL_SENDER_ADDRESS

        message = EmailMessage()
        message["From"] = f"{sender_name} <{sender_address}>"
        message["To"] = email_data.recipient
        message["Subject"] = f"{app_config.PROJECT_NAME} | {email_data.subject}"
        message.add_alternative(template.render(), subtype="html")

        await aiosmtplib.send(message, **self.smtp_config)

    async def queue(self, template: BaseTemplate, email_data: EmailData)  -> str:
        return await self.queue_service.push(
            task=SendEmail,
            data={"content": template.render(), "email_data": email_data},
        )

    async def send_plain(self, subject: str, recipient: str, body: str) -> None:
        message = EmailMessage()
        sender_name = app_config.EMAIL_SENDER_NAME
        sender_address = app_config.EMAIL_SENDER_ADDRESS

        message["From"] = f"{sender_name} <{sender_address}>"
        message["To"] = recipient
        message["Subject"] = f"{app_config.PROJECT_NAME} | {subject}"
        message.set_content(body)

        await aiosmtplib.send(message, **self.smtp_config)

    async def queue_plain(self, subject: str, recipient: str, body: str) -> str:
        email_data = {
            "subject": subject,
            "recipient": recipient,
            "sender_name": app_config.EMAIL_SENDER_NAME,
            "sender_address": app_config.EMAIL_SENDER_ADDRESS,
        }
        return await self.queue_service.push(
            task=SendEmail,
            data={"content": body, "email_data": email_data}
        )

