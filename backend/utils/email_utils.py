from flask_mail import Mail, Message
from jinja2 import Environment, PackageLoader, select_autoescape
import os


api_site = os.environ.get('VITE_API_POINT')
env = Environment(loader = PackageLoader('instance', 'templates'), autoescape=select_autoescape())
verification_email_template = env.get_template('verification_email_template.jinja')

mail_client = Mail()
verification_template = """
<!DOCTYPE html>
<html>
<head>
    <title>{action}</title>
</head>
<body>
    <h1>{action}</h1>
    <p>Click <a href="{api_site}/auth/verification/{token}">here</a> to verify your email</p>
</body>
"""

def verification_email_from_template(api_site: str, token: str):
    return verification_template.format(api_site=api_site, token=token, action="Verify your email")

def send_email(subject: str, html: str, to_addr: str, from_addr: str = "easylib@jesse-tong.work"):
    msg = Message(subject=subject, sender=from_addr, recipients=[to_addr], html=html)
    mail_client.send(msg)

async def send_verification_email(token: str, to_addr: str):
    email_html = verification_email_from_template(api_site, token)
    send_email("Verification email", email_html, to_addr=to_addr)