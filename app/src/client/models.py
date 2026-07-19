from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.src.utils.db import Base


class Client(Base):
    __tablename__ = "client"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    name = Column(String(200), nullable=False)
    address = Column(String(200), nullable=True)
    city = Column(String(50), nullable=True)
    gstin = Column(String(50), nullable=True)
    aadhar = Column(String(12), nullable=True)
    panno = Column(String(20), nullable=True)
    pincode = Column(String(6), nullable=True)
    mobile = Column(String(12), nullable=True)
    email = Column(String(255), nullable=True)
    state = Column(String(50), default="HARYANA", nullable=False)
    statecode = Column(String(2), default="06", nullable=False)
    currency = Column(String(3), default="INR", nullable=False)
    country = Column(String(150), default="India", nullable=False)

    # Relationship
    user = relationship("User", back_populates="clients")

    @property
    def full_address(self):
        return f"{self.name}, {self.address or ''}, {self.city or ''}"

    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.name}')>"
