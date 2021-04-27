from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from schemas import user_schema
import os

FRONTEND_URL_DEV = "localhost:3000/"

conf = ConnectionConfig(
    MAIL_USERNAME = "1fbe4db9ec5fa4",
    MAIL_PASSWORD ="6471c90a19c309",
    MAIL_FROM = "test@planetix.com",
    MAIL_PORT = 2525,
    MAIL_SERVER = "smtp.mailtrap.io",
    MAIL_TLS = True,
    MAIL_SSL = False
)

async def compose_email(user: user_schema.UserForgotPassword, password_reset_token: str):
    password_reset_link = FRONTEND_URL_DEV + "change-password/{0}".format(password_reset_token)
    template = """
        <html>
        <body>
            <p>Your password reset link is : <a href='{0}'>{0}</a>. <br>
            Please note it will expire in an hour.
            </p>
        </body>
        </html>
        """.format(password_reset_link)

    password_reset_mail = MessageSchema(
    subject = "Password Reset Request",
    recipients = [user.email],
    body = template,
    subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(password_reset_mail)

async def activation_email(user: user_schema.UserActivateAccount, account_activate_token: str):
    account_activation_link = FRONTEND_URL_DEV + "activate/{0}".format(account_activate_token)
    template = """
        <html>
        <body>
            <p>Your password reset link is : <a href='{0}'>{0}</a>. <br>
            Please note it will expire in an hour.
            </p>
        </body>
        </html>
        """.format(account_activate_token)

    account_activate_mail =  MessageSchema(
    subject = "Account activation",
    recipients = [user.email],
    body = template,
    subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(account_activate_mail)




