from fastapi.exceptions import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm.session import Session

from src.tasks.models import TaskModel
from src.tasks.schema import TaskCreateSchema, TaskUpdateSchema
from src.user.models import User


def create_task(body: TaskCreateSchema, db: Session, user: User):
    data = body.model_dump()
    data["user_id"] = user.id
    new_task = TaskModel(**data)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def get_tasks(db: Session):
    tasks = db.query(TaskModel).order_by(desc(TaskModel.id)).all()
    return tasks


def get_one_task(task_id: int, db: Session):
    one_task = db.get(TaskModel, task_id)
    if not one_task:
        raise HTTPException(404, detail=f"Task {task_id} not found!")

    return one_task


def update_task(body: TaskUpdateSchema, task_id: int, db: Session):
    one_task = db.get(TaskModel, task_id)
    if not one_task:
        raise HTTPException(404, detail=f"Task {task_id} not found!")

    data = body.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(one_task, field, value)

    db.commit()
    db.refresh(one_task)

    return one_task


def delete_task(task_id: int, db: Session):
    one_task = db.get(TaskModel, task_id)
    if not one_task:
        raise HTTPException(404, detail=f"Task {task_id} not found!")

    db.delete(one_task)
    db.commit()

    return None
