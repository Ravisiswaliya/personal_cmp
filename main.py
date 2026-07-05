from fastapi import FastAPI

# from src.tasks.models import TaskModel
from src.email.routes import email_routes
from src.tasks.router import task_routes
from src.user.routes import user_routes
from src.utils.db import Base, engine

Base.metadata.create_all(engine)


app = FastAPI(title="Getmax billing system")
app.include_router(task_routes, prefix="/api/v1")
app.include_router(user_routes, prefix="/api/v1")
app.include_router(email_routes, prefix="/api/v1")


@app.get("/")
def home():
    return {"msg": "my billing system"}
