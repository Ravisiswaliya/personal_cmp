from pydantic import BaseModel, ConfigDict


class TaskCreateSchema(BaseModel):
    title: str
    description: str
    is_completed: bool = False


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool | None = None


class TaskResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool
    user_id: int | None = 0

    model_config = ConfigDict(from_attributes=True)
