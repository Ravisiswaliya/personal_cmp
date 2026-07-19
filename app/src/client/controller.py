from fastapi.exceptions import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm.session import Session

from app.src.client.models import Client
from app.src.client.schema import (
    ClientCreateSchema,
    ClientFilter,
    ClientUpdateSchema,
)
from app.src.user.models import User


def get_client_or_404(client_id: int, user_id: int, db: Session) -> Client:
    client = (
        db.query(Client)
        .filter(
            Client.id == client_id,
            Client.user_id == user_id,
        )
        .first()
    )

    if client is None:
        raise HTTPException(
            status_code=404,
            detail=f"Client with id {client_id} not found.",
        )

    return client


def create_client(body: ClientCreateSchema, db: Session, user: User):
    data = body.model_dump()
    data["user_id"] = user.id
    new_client = Client(**data)

    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


def get_clients(filter: ClientFilter, db: Session, user: User):
    clients = db.query(Client).filter(Client.user_id == user.id)
    if filter.name:
        clients = clients.filter(Client.name.ilike(f"%{filter.name}%"))

    if filter.city:
        clients = clients.filter(Client.city == filter.city)

    if filter.address:
        clients = clients.filter(Client.address.ilike(f"%{filter.address}%"))

    total = clients.count()

    # Pagination
    clients = (
        clients.order_by(Client.id.desc())
        .offset((filter.page - 1) * filter.page_size)
        .limit(filter.page_size)
        .all()
    )

    return {
        "items": clients,
        "pagination": {
            "page": filter.page,
            "page_size": filter.page_size,
            "total": total,
            "total_pages": (total + filter.page_size - 1) // filter.page_size,
            "has_next": filter.page * filter.page_size < total,
            "has_previous": filter.page > 1,
        },
    }


def get_one_client(client_id: int, db: Session, user: User) -> Client:
    return get_client_or_404(client_id, user.id, db)


def update_client(
    body: ClientUpdateSchema,
    client_id: int,
    db: Session,
    user: User,
) -> Client:
    client = get_client_or_404(client_id, user.id, db)

    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(client, key, value)

    db.commit()
    db.refresh(client)

    return client


def delete_client(client_id: int, db: Session, user: User) -> None:
    client = get_client_or_404(client_id, user.id, db)
    db.delete(client)
    db.commit()
