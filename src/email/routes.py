from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, UploadFile, status
from pydantic.networks import EmailStr
from starlette import status

from src.email.helper import render_template
from src.email.schema import InvoiceEmailData, SendInvoiceEmailSchema
from src.email.service import send_email

email_routes = APIRouter(prefix="/email", tags=["Email"])


@email_routes.post(
    "/send",
    status_code=status.HTTP_201_CREATED,
)
async def send_simple_email(body: SendInvoiceEmailSchema):
    html = render_template(
        "invoice.html",
        body.invoice.model_dump(mode="json"),
    )

    await send_email(
        emails=body.recipients,
        cc=body.cc,
        bcc=body.bcc,
        subject=body.subject,
        html_content=html,
    )

    return {
        "success": True,
        "message": "Invoice email sent successfully",
    }


@email_routes.post(
    "/send",
    status_code=status.HTTP_201_CREATED,
)
@email_routes.post("/send")
async def send_email(
    background_tasks: BackgroundTasks,
    invoice: Annotated[
        InvoiceEmailData,
        Depends(InvoiceEmailData.as_form),
    ],
    subject: str = Form(...),
    recipients: list[EmailStr] = Form(...),
    cc: list[EmailStr] = Form([]),
    bcc: list[EmailStr] = Form([]),
    attachments: list[UploadFile] = File([]),
):
    html = render_template(
        "invoice.html",
        invoice.model_dump(mode="json"),
    )

    await send_email(
        emails=recipients,
        cc=cc,
        bcc=bcc,
        subject=subject,
        html_content=html,
        attachments=attachments,
        background_tasks=background_tasks,
    )

    return {"success": True}
