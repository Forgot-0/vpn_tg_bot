from dataclasses import dataclass

from app.application.interfaces.mail import BaseMailService, EmailData
from app.application.interfaces.queue import QueueService
from app.configs.smtp import SMTPConfig
from app.infrastructure.services.mail.task import SendEmail
from app.infrastructure.services.mail.templates.base import ResetPasswordTemplate, VerifyEmailTemplate



@dataclass
class AioSmtpLibMailService(BaseMailService):
    smtp_config: SMTPConfig
    queue_service: QueueService

    async def send_raw(self, content: str, email_data: EmailData) -> str | None:
        data = {
            "content": content,
            "email_data": {
                "subject": email_data.subject,
                "recipient": email_data.recipient,
                "sender_address": email_data.sender_address,
                "sender_name": email_data.sender_name,
            },
        }

        task_id = await self.queue_service.push(SendEmail, data)
        return task_id

    async def send_verification_code(self, email: str, code: str, valid_minutes: int) -> str | None:
        template = VerifyEmailTemplate(email, code)
        email_data = EmailData(subject="Verify your email", recipient=email)
        return await self.send_template_content(template.render(), email_data)

    async def send_reset_code(self, email: str, code: str, valid_minutes: int) -> str | None:
        template = ResetPasswordTemplate(email, code, valid_minutes)
        email_data = EmailData(subject="Password reset", recipient=email)
        return await self.send_template_content(template.render(), email_data)

    async def send_template_content(self, content: str, email_data: EmailData) -> str | None:
        data = {
            "content": content,
            "email_data": {
                "subject": email_data.subject,
                "recipient": email_data.recipient,
                "sender_address": email_data.sender_address,
                "sender_name": email_data.sender_name,
            },
        }
        task_id = await self.queue_service.push(SendEmail, data)
        return task_id
