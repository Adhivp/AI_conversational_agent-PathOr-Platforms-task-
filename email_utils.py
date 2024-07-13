import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import formataddr
from dotenv import load_dotenv
import os
import schedule
import time
from datetime import datetime

load_dotenv()

def send_email(to_address, subject, body, attachment_path, attachment_name, send_datetime=None):
    """
    Sends an email with a PDF attachment.

    :param to_address: Recipient's email address.
    :param subject: Subject of the email.
    :param body: Body text of the email.
    :param attachment_path: File path of the PDF attachment.
    :param attachment_name: Name of the PDF attachment.
    :param send_datetime: Optional datetime object to schedule the email.
    """
    from_address = os.getenv('EMAIL_ADDRESS')
    password = os.getenv('EMAIL_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT'))

    msg = MIMEMultipart()
    msg['From'] = formataddr(('Sender Name', from_address))
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with open(attachment_path, "rb") as attachment:
        part = MIMEApplication(attachment.read(), Name=attachment_name)
    part['Content-Disposition'] = f'attachment; filename="{attachment_name}"'
    msg.attach(part)

    def send():
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_address, password)
        server.sendmail(from_address, to_address, msg.as_string())
        server.quit()

    if send_datetime:
        delay = (send_datetime - datetime.now()).total_seconds()
        if delay > 0:
            time.sleep(delay)
            send()
    else:
        send()
