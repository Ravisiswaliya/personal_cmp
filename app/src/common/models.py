from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.src.utils.db import Base


class AuthStampedModel:
    """
    Abstract mixin for created_by and modified_by
    """

    created_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    modified_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    created_by = relationship("User", foreign_keys=[created_by_id])

    modified_by = relationship("User", foreign_keys=[modified_by_id])


class TimeStampModel:
    """Abstract Timestamp Model"""

    cdate: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    udate: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
