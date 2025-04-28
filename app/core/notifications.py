import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
import logging

logger = logging.getLogger("tasktodo")

class EmailNotification:
    def __init__(self, smtp_host: str, smtp_port: int, smtp_user: str, smtp_password: str):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    async def send_task_notification(
        self,
        to_email: str,
        task_title: str,
        task_description: str,
        due_date: str
    ):
        message = MIMEMultipart()
        message["From"] = self.smtp_user
        message["To"] = to_email
        message["Subject"] = f"Task Reminder: {task_title}"

        body = f"""
        <html>
            <body>
                <h2>Task Reminder</h2>
                <p><strong>Title:</strong> {task_title}</p>
                <p><strong>Description:</strong> {task_description}</p>
                <p><strong>Due Date:</strong> {due_date}</p>
            </body>
        </html>
        """
        message.attach(MIMEText(body, "html"))

        try:
            async with aiosmtplib.SMTP(
                hostname=self.smtp_host,
                port=self.smtp_port,
                use_tls=True
            ) as smtp:
                await smtp.login(self.smtp_user, self.smtp_password)
                await smtp.send_message(message)
                logger.info(f"Notification email sent to {to_email}")
        except Exception as e:
            logger.error(f"Failed to send notification email: {str(e)}")
            raise

# Create notification instance with environment variables
notification = EmailNotification(
    smtp_host="smtp.gmail.com",
    smtp_port=587,
    smtp_user="your-email@gmail.com",  # Replace with your email
    smtp_password="your-app-password"  # Replace with your app password
) 