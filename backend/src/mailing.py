import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import config
from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    email: EmailStr
    subject: str
    message: str


def send_email(email: EmailSchema):
    msg = MIMEMultipart()
    msg["From"] = config.SMTP_USERNAME
    msg["To"] = email.email
    msg["Subject"] = email.subject

    msg.attach(MIMEText(email.message, "plain"))

    try:
        server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
        server.starttls()
        server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
        server.sendmail(config.SMTP_USERNAME, email.email, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
