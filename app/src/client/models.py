from typing import List

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.src.invoice.models import InvoiceDetail, QuotationDetail
from app.src.user.models import User
from app.src.utils.db import Base


class Client(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, index=True
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    address: Mapped[str | None] = mapped_column(String(200), nullable=True)
    city: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gstin: Mapped[str | None] = mapped_column(String(50), nullable=True)
    aadhar: Mapped[str | None] = mapped_column(String(12), nullable=True)
    panno: Mapped[str | None] = mapped_column(String(20), nullable=True)
    pincode: Mapped[str | None] = mapped_column(String(6), nullable=True)
    mobile: Mapped[str | None] = mapped_column(String(12), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    state: Mapped[str] = mapped_column(String(50), default="HARYANA", nullable=False)
    statecode: Mapped[str] = mapped_column(String(2), default="06", nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR", nullable=False)
    country: Mapped[str] = mapped_column(String(150), default="India", nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(
        back_populates="clients",
    )

    invoices: Mapped[List["InvoiceDetail"]] = relationship(
        back_populates="client", cascade="all, delete-orphan"
    )

    quotations: Mapped[List["QuotationDetail"]] = relationship(
        back_populates="client", cascade="all, delete-orphan"
    )

    @property
    def full_address(self) -> str:
        return f"{self.name}, {self.address or ''}, {self.city or ''}"

    def __repr__(self) -> str:
        return f"<Client(id={self.id}, name='{self.name}')>"
