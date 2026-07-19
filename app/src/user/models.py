from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.src.utils.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    tasks = relationship(
        "TaskModel",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    clients = relationship(
        "Client",
        back_populates="user",
        cascade="all, delete-orphan",
    )
