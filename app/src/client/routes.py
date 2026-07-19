from typing import List

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm.session import Session

from app.src.client import controller
from app.src.client.schema import (
    ClientCreateSchema,
    ClientFilter,
    ClientListResponseSchema,
    ClientResponseSchema,
    ClientUpdateSchema,
)
from app.src.utils.db import get_db
from app.src.utils.helpers import is_authenticated

client_routes = APIRouter(prefix="/clients", tags=["Clients"])


@client_routes.post(
    "/create",
    response_model=ClientResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_client(
    body: ClientCreateSchema, db=Depends(get_db), user=Depends(is_authenticated)
):
    return controller.create_client(body, db, user)


@client_routes.get(
    "/all_clients",
    response_model=ClientListResponseSchema,
    status_code=status.HTTP_200_OK,
)
def get_all_clients(
    filter: ClientFilter = Depends(),
    db: Session = Depends(get_db),
    user=Depends(is_authenticated),
):
    return controller.get_clients(filter, db, user)


@client_routes.put(
    "/update_client/{client_id}",
    response_model=ClientResponseSchema,
    status_code=status.HTTP_200_OK,
)
def update_client(
    body: ClientUpdateSchema,
    client_id: int,
    db: Session = Depends(get_db),
    user=Depends(is_authenticated),
):
    return controller.update_client(body, client_id, db, user)


@client_routes.delete(
    "/delete_client/{client_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_client(
    client_id: int, db: Session = Depends(get_db), user=Depends(is_authenticated)
):
    return controller.delete_client(client_id, db, user)
