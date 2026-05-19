import smtplib
from email.mime.text import MIMEText

# Gmail SMTP Configuration (Using SSL on Port 465)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # SSL port
SMTP_USER = "jana.sneznik@gmail.com"  # Your Gmail address
SMTP_PASSWORD = "nutrie69"  # Your Gmail password or App password

def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    # Establish SSL connection to SMTP server
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
