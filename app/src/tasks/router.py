from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm.session import Session

from app.src.tasks import controller
from app.src.tasks.schema import TaskCreateSchema, TaskResponseSchema, TaskUpdateSchema
from app.src.user.models import User
from app.src.utils.db import get_db
from app.src.utils.helpers import is_authenticated

task_routes = APIRouter(prefix="/tasks", tags=["Task"])


@task_routes.post(
    "/create",
    response_model=TaskResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    body: TaskCreateSchema,
    db=Depends(get_db),
    user=Depends(is_authenticated),
):
    return controller.create_task(body, db, user)


@task_routes.get(
    "/all_tasks",
    response_model=List[TaskResponseSchema],
    status_code=status.HTTP_200_OK,
)
def get_all_tasks(
    db: Session = Depends(get_db),
    user=Depends(is_authenticated),
):
    return controller.get_tasks(db)


@task_routes.get(
    "/get_task/{task_id}",
    response_model=TaskResponseSchema,
    status_code=status.HTTP_200_OK,
)
def get_one_tasks(
    task_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(is_authenticated),
):
    return controller.get_one_task(task_id, db)


@task_routes.put(
    "/update_task/{task_id}",
    response_model=TaskResponseSchema,
    status_code=status.HTTP_200_OK,
)
def update_task(
    body: TaskUpdateSchema,
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(is_authenticated),
):
    return controller.update_task(body, task_id, db)


@task_routes.delete("/delete_task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(is_authenticated),
):
    return controller.delete_task(task_id, db)
