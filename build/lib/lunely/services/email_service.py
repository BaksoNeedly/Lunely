import smtplib
from email.message import EmailMessage

class EmailService:

    _email: str | None = None
    _password: str | None = None

    @classmethod
    def configure(cls, email: str, password: str) -> None:
        """Configure the SMTP sender from the host application's settings."""
        cls._email = email
        cls._password = password

    @classmethod
    def send(
        cls,
        receiver_email: str,
        subject: str,
        message: str
    ) -> bool:
        if not cls._email or not cls._password:
            raise RuntimeError("[EMAIL] EmailService has not been configured.")

        mail = EmailMessage()
        mail["From"] = cls._email
        mail["To"] = receiver_email
        mail["Subject"] = subject
        mail.set_content(message)
        
        try:
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(cls._email, cls._password)
                server.send_message(mail)
                return True
        except:
            return False
