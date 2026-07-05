from datetime import date
from decimal import Decimal

from fastapi import Form
from pydantic import BaseModel, ConfigDict, EmailStr


class InvoiceEmailData(BaseModel):
    customer_name: str
    invoice_number: str
    invoice_date: date
    due_date: date
    currency: str
    amount: Decimal
    company_name: str
    sender_name: str

    @classmethod
    def as_form(
        cls,
        customer_name: str = Form(...),
        invoice_number: str = Form(...),
        invoice_date: date = Form(...),
        due_date: date = Form(...),
        currency: str = Form(...),
        amount: Decimal = Form(...),
        company_name: str = Form(...),
        sender_name: str = Form(...),
    ):
        return cls(
            customer_name=customer_name,
            invoice_number=invoice_number,
            invoice_date=invoice_date,
            due_date=due_date,
            currency=currency,
            amount=amount,
            company_name=company_name,
            sender_name=sender_name,
        )


class EmailEnvelope(BaseModel):
    recipients: list[EmailStr]
    cc: list[EmailStr] = []
    bcc: list[EmailStr] = []
    subject: str


class SendInvoiceEmailSchema(EmailEnvelope):
    invoice: InvoiceEmailData
