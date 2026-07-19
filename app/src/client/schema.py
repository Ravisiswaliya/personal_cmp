import re
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

# GSTIN
GSTIN_REGEX = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$")

# PAN
PAN_REGEX = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")

# Aadhaar
AADHAAR_REGEX = re.compile(r"^[2-9][0-9]{11}$")


def validate_pan_format(pan: str) -> bool:
    return bool(PAN_REGEX.fullmatch(pan.strip().upper()))


def validate_aadhaar_format(aadhaar: str) -> bool:
    return bool(AADHAAR_REGEX.fullmatch(aadhaar.strip()))


def validate_gstin_format(gstin: str) -> bool:
    return bool(GSTIN_REGEX.fullmatch(gstin.strip().upper()))


class ClientFilter(BaseModel):
    name: str | None = None
    city: str | None = None
    address: str | None = None

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)


class ClientCreateSchema(BaseModel):
    name: str
    address: str
    city: str
    gstin: str | None = None
    aadhar: str | None = None
    panno: str | None = None

    pincode: str | None = None
    mobile: str | None = None
    email: EmailStr | None = None

    state: str | None = None
    statecode: str | None = None
    currency: str | None = None
    country: str | None = None

    @field_validator("gstin")
    @classmethod
    def validate_gstin(cls, value: Optional[str]) -> Optional[str]:
        if not value:
            return value

        value = value.strip().upper()

        if not validate_gstin_format(value):
            raise ValueError("Invalid GSTIN format")

        return value

    @field_validator("panno")
    @classmethod
    def validate_pan(cls, value):
        if not value:
            return value

        value = value.strip().upper()

        if not validate_pan_format(value):
            raise ValueError("Invalid PAN Number")

        return value

    @field_validator("aadhar")
    @classmethod
    def validate_aadhaar(cls, value):
        if not value:
            return value

        value = value.strip()

        if not validate_aadhaar_format(value):
            raise ValueError("Invalid Aadhaar Number")

        return value


class ClientUpdateSchema(BaseModel):
    name: str | None
    address: str | None
    city: str | None
    gstin: str | None = None
    aadhar: str | None = None
    panno: str | None = None
    pincode: str | None = None
    mobile: str | None = None
    email: EmailStr | None = None
    state: str | None = None
    statecode: str | None = None
    currency: str | None = None
    country: str | None = None


class ClientResponseSchema(BaseModel):
    id: int
    name: str
    address: str
    city: str
    gstin: str | None
    aadhar: str | None
    panno: str | None
    pincode: str | None
    mobile: str | None
    email: EmailStr | None
    state: str | None
    statecode: str | None
    currency: str | None
    country: str | None
    user_id: int | None = 0

    model_config = ConfigDict(from_attributes=True)


class PaginationSchema(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    has_next: bool
    has_previous: bool


class ClientListResponseSchema(BaseModel):
    items: list[ClientResponseSchema]
    pagination: PaginationSchema
