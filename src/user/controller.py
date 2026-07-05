from fastapi.exceptions import HTTPException
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session

from src.user.auth import create_access_token, get_password_hash, verify_password
from src.user.models import User
from src.user.schema import UserCreateSchema, UserLoginSchema


def login_user(body: UserLoginSchema, db: Session):
    user = db.query(User).filter(User.username == body.username).first()
    if not user:
        raise HTTPException(404, detail="Username not exists!")

    if not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Wrong Password!")

    # create token
    token = create_access_token(user)

    return {
        "token": token,
    }


def register(body: UserCreateSchema, db: Session):
    # if already exists
    # email unique check

    existing_user = (
        db.query(User)
        .filter(
            or_(
                User.username == body.username,
                User.email == body.email,
            )
        )
        .first()
    )

    if existing_user:
        if existing_user.username == body.username:
            raise HTTPException(status_code=400, detail="Username already exists")

        raise HTTPException(status_code=400, detail="Email already exists")

    data = body.model_dump()
    data["password_hash"] = get_password_hash(body.password)
    del data["password"]

    new_user = User(**data)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")

    return new_user
