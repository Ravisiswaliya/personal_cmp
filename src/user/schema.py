from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    name: str
    username: str
    password: str
    email: str


class UserResponseSchema(BaseModel):
    id: int
    name: str
    username: str
    email: str
    is_active: bool


class UserLoginSchema(BaseModel):
    username: str
    password: str
