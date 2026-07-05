from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Request
from fastapi.exceptions import HTTPException
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy.orm.session import Session

from src.user.models import User
from src.utils.settings import settings

password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(user):
    exp_time = datetime.now(timezone.utc) + timedelta(
        minutes=settings.TOKEN_EXPIRE_TIME
    )
    token = jwt.encode(
        {"_id": user.id, "exp": exp_time}, settings.SECRET_KEY, settings.ALGORITHM
    )
    return token
