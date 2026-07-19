from datetime import date
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# ProductItems
# ---------------------------------------------------------------------------


class ProductItemBase(BaseModel):
    hsncode: Optional[str] = Field(None, max_length=30)
    sgst: Optional[Decimal] = Field(None, description="SGST rate in percent")
    cgst: Optional[Decimal] = Field(None, description="CGST rate in percent")
    igst: Optional[Decimal] = Field(None, description="IGST rate in percent")
    product_discription: Optional[str] = Field(None, max_length=30)
    product_quantity: Optional[Decimal] = None
    unit_type: Optional[str] = Field(None, max_length=30)
    unit_price: Optional[Decimal] = None


class ProductItemCreate(ProductItemBase):
    """Used when creating a product line item nested under an invoice
    or quotation. invoice_id / qtsn_id are set by the parent endpoint,
    not supplied directly by the client.
    """

    pass


class ProductItemUpdate(BaseModel):
    hsncode: Optional[str] = Field(None, max_length=30)
    sgst: Optional[Decimal] = None
    cgst: Optional[Decimal] = None
    igst: Optional[Decimal] = None
    product_discription: Optional[str] = Field(None, max_length=30)
    product_quantity: Optional[Decimal] = None
    unit_type: Optional[str] = Field(None, max_length=30)
    unit_price: Optional[Decimal] = None


class ProductItemRead(ProductItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    invoice_id: Optional[int] = None
    qtsn_id: Optional[int] = None

    # computed / property fields from the ORM model, rounded to 2 decimals
    get_sgst_amount: Optional[Decimal] = None
    get_cgst_amount: Optional[Decimal] = None
    get_igst_amount: Optional[Decimal] = None
    single_item_total_gst: Optional[Decimal] = None
    single_item_total_amount_without_tax: Optional[Decimal] = None
    single_item_total_amount_after_tax: Optional[Decimal] = None


# ---------------------------------------------------------------------------
# InvoiceDetail
# ---------------------------------------------------------------------------


class InvoiceBase(BaseModel):
    invoice_no: str = Field(..., max_length=30)
    client_id: int
    orderno: Optional[str] = Field(None, max_length=100)
    invoice_date: date
    transportmode: Optional[str] = Field(None, max_length=100)
    vehicleno: Optional[str] = Field(None, max_length=50)
    dateofsupply: Optional[date] = None
    placeofsupply: Optional[str] = Field(None, max_length=50)
    gstrc: Optional[Decimal] = None
    tc: Optional[str] = None
    round_off: Optional[Decimal] = None
    is_paid: bool = False


class InvoiceCreate(InvoiceBase):
    products: List[ProductItemCreate] = Field(default_factory=list)


class InvoiceUpdate(BaseModel):
    invoice_no: Optional[str] = Field(None, max_length=30)
    client_id: Optional[int] = None
    orderno: Optional[str] = Field(None, max_length=100)
    invoice_date: Optional[date] = None
    transportmode: Optional[str] = Field(None, max_length=100)
    vehicleno: Optional[str] = Field(None, max_length=50)
    dateofsupply: Optional[date] = None
    placeofsupply: Optional[str] = Field(None, max_length=50)
    gstrc: Optional[Decimal] = None
    tc: Optional[str] = None
    round_off: Optional[Decimal] = None
    is_paid: Optional[bool] = None
    products: Optional[List[ProductItemCreate]] = None


class InvoiceRead(InvoiceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    products: List[ProductItemRead] = Field(default_factory=list)


class InvoiceListItem(BaseModel):
    """Lightweight schema for list/table views."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    invoice_no: str
    invoice_date: date
    client_id: int
    is_paid: bool


# ---------------------------------------------------------------------------
# QuotationDetail
# ---------------------------------------------------------------------------


class QuotationBase(BaseModel):
    qtsn_no: str = Field(..., max_length=30)
    qtsn_date: date
    subject: str = Field(..., max_length=500)
    client_id: int
    round_off: Optional[Decimal] = None
    tc: Optional[str] = None


class QuotationCreate(QuotationBase):
    products: List[ProductItemCreate] = Field(default_factory=list)


class QuotationUpdate(BaseModel):
    qtsn_no: Optional[str] = Field(None, max_length=30)
    qtsn_date: Optional[date] = None
    subject: Optional[str] = Field(None, max_length=500)
    client_id: Optional[int] = None
    round_off: Optional[Decimal] = None
    tc: Optional[str] = None
    products: Optional[List[ProductItemCreate]] = None


class QuotationRead(QuotationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    products: List[ProductItemRead] = Field(default_factory=list)


class QuotationListItem(BaseModel):
    """Lightweight schema for list/table views."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    qtsn_no: str
    qtsn_date: date
    subject: str
    client_id: int
