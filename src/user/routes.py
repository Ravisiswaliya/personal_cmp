from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm.session import Session

from src.user import controller
from src.user.schema import UserCreateSchema, UserLoginSchema, UserResponseSchema
from src.utils.db import get_db
from src.utils.helpers import is_authenticated

user_routes = APIRouter(prefix="/user")


@user_routes.post(
    "/register",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def register(
    body: UserCreateSchema,
    db: Session = Depends(get_db),
):
    return controller.register(body, db)


@user_routes.post(
    "/login",
    # response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
)
def login(body: UserLoginSchema, db: Session = Depends(get_db)):
    return controller.login_user(body, db)


@user_routes.post(
    "/get-profile",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
)
def check_token(request: Request, db: Session = Depends(get_db)):
    return is_authenticated(request, db)
