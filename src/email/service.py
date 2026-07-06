from fastapi import HTTPException, UploadFile
from fastapi_mail import (
    ConnectionConfig,
    FastMail,
    MessageSchema,
    MessageType,
)
from pydantic import EmailStr

from src.email.schema import EmailEnvelope, InvoiceEmailData, SendInvoiceEmailSchema
from src.utils.settings import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.GMAIL_USERNAME,
    MAIL_PASSWORD=settings.GOOGLE_APP_PASSWORD,
    MAIL_FROM=settings.GMAIL_USERNAME,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Ravi Siswaliya",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

fm = FastMail(conf)


async def send_email(
    body: EmailEnvelope,
    html_content: str,
) -> None:
    message = MessageSchema(
        subject=body.subject,
        recipients=[str(email) for email in body.recipients],
        cc=[str(email) for email in body.cc],
        bcc=[str(email) for email in body.bcc],
        body=html_content,
        subtype=MessageType.html,
    )

    try:
        await fm.send_message(message)
        print("Email send successfully ++++++++++++++++++++++")

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email: {exc}",
        )


async def send_email_with_attachment(
    emails: list[EmailStr],
    subject: str,
    html_content: str,
    cc: list[EmailStr] | None = None,
    bcc: list[EmailStr] | None = None,
    attachments: list[UploadFile] | None = None,
):
    message = MessageSchema(
        subject=subject,
        recipients=[str(i) for i in emails],
        cc=[str(i) for i in cc] if cc else [],
        bcc=[str(i) for i in bcc] if bcc else [],
        body=html_content,
        subtype=MessageType.html,
        attachments=attachments or [],
    )

    try:
        await fm.send_message(message)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
