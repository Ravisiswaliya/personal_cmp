from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import List

from sqlalchemy import Boolean, Date, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.src.client.models import Client
from app.src.common.models import AuthStampedModel, TimeStampModel
from app.src.utils.db import Base


class InvoiceDetail(Base, AuthStampedModel, TimeStampModel):
    __tablename__ = "invoice"

    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_no: Mapped[str] = mapped_column(String(30), unique=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"))
    orderno: Mapped[str | None] = mapped_column(String(100), nullable=True)
    invoice_date: Mapped[date] = mapped_column(Date)
    transportmode: Mapped[str | None] = mapped_column(String(100), nullable=True)
    vehicleno: Mapped[str | None] = mapped_column(String(50), nullable=True)
    dateofsupply: Mapped[date | None] = mapped_column(Date, nullable=True)
    placeofsupply: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gstrc: Mapped[Decimal | None] = mapped_column(Float, nullable=True)
    tc: Mapped[str] = mapped_column(
        Text,
        default="All Disputes subject to Hisar Jurisdiction."
        "Goods once sold will not be taken back or "
        "exchanged.Interest @24 will be charged if bills"
        " not paid at presentation. E.& O.E.",
    )

    round_off: Mapped[Decimal | None] = mapped_column(Float, nullable=True)

    is_paid: Mapped[bool] = mapped_column(Boolean, default=False)

    client: Mapped["Client"] = relationship(back_populates="invoices")

    products: Mapped[List["ProductItems"]] = relationship(
        back_populates="invoice",
        cascade="all, delete-orphan",
    )


class ProductItems(Base):
    __tablename__ = "products_item"

    id: Mapped[int] = mapped_column(primary_key=True)

    invoice_id: Mapped[int | None] = mapped_column(
        ForeignKey("invoice.id"), nullable=True
    )

    qtsn_id: Mapped[int | None] = mapped_column(
        ForeignKey("quotation.id"), nullable=True
    )

    hsncode: Mapped[str] = mapped_column(String(30), nullable=True)
    sgst: Mapped[Decimal] = mapped_column(Float, nullable=True)
    cgst: Mapped[Decimal] = mapped_column(Float, nullable=True)
    igst: Mapped[Decimal] = mapped_column(Float, nullable=True)
    product_discription: Mapped[str] = mapped_column(String(30), nullable=True)
    product_quantity: Mapped[Decimal] = mapped_column(Float, nullable=True)
    unit_type: Mapped[str] = mapped_column(String(30), nullable=True)
    unit_price: Mapped[Decimal] = mapped_column(Float, nullable=True)

    invoice: Mapped["InvoiceDetail"] = relationship(back_populates="products")
    quotation: Mapped["QuotationDetail"] = relationship(back_populates="products")

    TWO_PLACES = Decimal("0.01")

    @staticmethod
    def _to_decimal(value) -> Decimal:
        """Safely coerce a value (int/float/Decimal/None) to Decimal."""
        if value is None:
            return Decimal("0")
        if isinstance(value, Decimal):
            return value
        return Decimal(str(value))

    def _quantize(self, value: Decimal) -> Decimal:
        """Round a Decimal to exactly 2 decimal places using standard
        currency rounding (round-half-up), avoiding float precision errors.
        """
        return value.quantize(self.TWO_PLACES, rounding=ROUND_HALF_UP)

    @property
    def get_sgst_amount(self) -> Decimal:
        sgst = self._to_decimal(self.sgst)
        unit_price = self._to_decimal(self.unit_price)
        quantity = self._to_decimal(self.product_quantity)
        amount = (sgst * unit_price * quantity) / Decimal("100")
        return self._quantize(amount)

    @property
    def get_cgst_amount(self) -> Decimal:
        cgst = self._to_decimal(self.cgst)
        unit_price = self._to_decimal(self.unit_price)
        quantity = self._to_decimal(self.product_quantity)
        amount = (cgst * unit_price * quantity) / Decimal("100")
        return self._quantize(amount)

    @property
    def get_igst_amount(self) -> Decimal:
        igst = self._to_decimal(self.igst)
        unit_price = self._to_decimal(self.unit_price)
        quantity = self._to_decimal(self.product_quantity)
        amount = (igst * unit_price * quantity) / Decimal("100")
        return self._quantize(amount)

    @property
    def single_item_total_gst(self) -> Decimal:
        total_gst_rate = (
            self._to_decimal(self.cgst)
            + self._to_decimal(self.sgst)
            + self._to_decimal(self.igst)
        )
        unit_price = self._to_decimal(self.unit_price)
        quantity = self._to_decimal(self.product_quantity)
        amount = (total_gst_rate * unit_price * quantity) / Decimal("100")
        return self._quantize(amount)

    @property
    def single_item_total_amount_without_tax(self) -> Decimal:
        unit_price = self._to_decimal(self.unit_price)
        quantity = self._to_decimal(self.product_quantity)
        amount = unit_price * quantity
        return self._quantize(amount)

    @property
    def single_item_total_amount_after_tax(self) -> Decimal:
        total_gst_rate = (
            self._to_decimal(self.cgst)
            + self._to_decimal(self.sgst)
            + self._to_decimal(self.igst)
        )
        unit_price = self._to_decimal(self.unit_price)
        quantity = self._to_decimal(self.product_quantity)
        gst_amount = (total_gst_rate * unit_price * quantity) / Decimal("100")
        item_price = quantity * unit_price
        return self._quantize(gst_amount + item_price)


class QuotationDetail(Base, AuthStampedModel, TimeStampModel):
    __tablename__ = "quotation"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    qtsn_no: Mapped[str] = mapped_column(String(30), unique=True)
    qtsn_date: Mapped[date] = mapped_column(Date)
    subject: Mapped[str] = mapped_column(String(500), unique=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"))

    round_off: Mapped[Decimal | None] = mapped_column(Float, nullable=True)

    tc: Mapped[str] = mapped_column(
        Text,
        default="1. 100% ADVANCE \
        2. Service with 7 days after order confirmation \
        3.Quoted Rate validity is 30 Days from the date of quotation",
    )

    client: Mapped["Client"] = relationship(back_populates="quotations")

    products: Mapped[List["ProductItems"]] = relationship(
        back_populates="quotation",
        cascade="all, delete-orphan",
    )
