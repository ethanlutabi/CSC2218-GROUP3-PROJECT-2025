from application.transfer_logging.notifications_services import NotificationAdapterInterface
from application.transfer_logging.logging_service import LoggerInterface
import smtplib
from email.message import EmailMessage

class ConsoleNotificationAdapter(NotificationAdapterInterface):
    """Simple adapter that writes notifications to the console."""
    def send_email(self, recipient: str, subject: str, body: str) -> None:
        print(f"[EMAIL] To: {recipient} | Subject: {subject} | Body: {body}")

    def send_sms(self, number: str, message: str) -> None:
        print(f"[SMS] To: {number} | Message: {message}")

class SMTPNotificationAdapter(NotificationAdapterInterface):
    """
    Example real adapter using smtplib.
    You'd configure SMTP settings (host, port, credentials) at startup.
    """
    def __init__(self, smtp_host: str, smtp_port: int, username: str, password: str):


        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._username = username
        self._password = password
        self._smtp = smtplib.SMTP(self._smtp_host, self._smtp_port)
        self._smtp.starttls()
        self._smtp.login(self._username, self._password)

    def send_email(self, recipient: str, subject: str, body: str) -> None:
        msg = EmailMessage()
        msg["From"] = self._username
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.set_content(body)
        self._smtp.send_message(msg)

    def send_sms(self, number: str, message: str) -> None:
        # If you integrate with an SMS gateway, call its API here.
        # For now, we’ll just print:
        print(f"[SMS via gateway] To: {number} | Message: {message}")


