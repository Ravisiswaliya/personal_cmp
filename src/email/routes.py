from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, UploadFile, status
from pydantic.networks import EmailStr
from starlette import status

from src.email.helper import render_template
from src.email.schema import InvoiceEmailData, SendInvoiceEmailSchema
from src.email.service import send_email

email_routes = APIRouter(prefix="/email", tags=["Email"])


@email_routes.post(
    "/send-simple-email",
    status_code=status.HTTP_201_CREATED,
)
async def send_simple_email(
    body: SendInvoiceEmailSchema,
    background_tasks: BackgroundTasks,
):
    email_data = body.invoice.model_dump()
    html = render_template("invoice.html", email_data)

    background_tasks.add_task(send_email, body, html)

    print("email sent")

    return {
        "success": True,
        "message": "Invoice email sent successfully",
    }


# @email_routes.post(
#     "/send",
#     status_code=status.HTTP_201_CREATED,
# )
# @email_routes.post("/send")
# async def send_email(
#     background_tasks: BackgroundTasks,
#     invoice: Annotated[
#         InvoiceEmailData,
#         Depends(InvoiceEmailData.as_form),
#     ],
#     subject: str = Form(...),
#     recipients: list[EmailStr] = Form(...),
#     cc: list[EmailStr] = Form([]),
#     bcc: list[EmailStr] = Form([]),
#     attachments: list[UploadFile] = File([]),
# ):
#     html = render_template(
#         "invoice.html",
#         invoice.model_dump(mode="json"),
#     )

#     email_res = await send_email(
#         emails=recipients,
#         cc=cc,
#         bcc=bcc,
#         subject=subject,
#         html_content=html,
#         attachments=attachments,
#     )

#     background_tasks.add_task(email_res)

#     return {"success": True}
