import smtplib
from email.mime.text import MIMEText
import os

def send_email(subject, body, to_addr, from_addr=None, smtp_server=None, smtp_port=587, login=None, password=None):
    from_addr = from_addr or os.environ.get("EMAIL_FROM")
    smtp_server = smtp_server or os.environ.get("SMTP_SERVER")
    smtp_port = int(smtp_port or os.environ.get("SMTP_PORT", 587))
    login = login or os.environ.get("SMTP_LOGIN")
    password = password or os.environ.get("SMTP_PASSWORD")
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(login, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())