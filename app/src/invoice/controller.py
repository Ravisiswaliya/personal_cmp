from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.src.invoice import models, schemas
from app.src.utils.db import get_db

router = APIRouter(prefix="/invoices", tags=["Invoices"])


def _get_invoice_or_404(db: Session, invoice_id: int) -> models.InvoiceDetail:
    invoice = (
        db.query(models.InvoiceDetail)
        .filter(models.InvoiceDetail.id == invoice_id)
        .first()
    )
    if invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invoice with id {invoice_id} not found",
        )
    return invoice


@router.post(
    "",
    response_model=schemas.InvoiceRead,
    status_code=status.HTTP_201_CREATED,
)
def create_invoice(payload: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    """Create a new invoice, optionally with nested product line items."""
    invoice_data = payload.model_dump(exclude={"products"})
    invoice = models.InvoiceDetail(**invoice_data)

    for product in payload.products:
        invoice.products.append(models.ProductItems(**product.model_dump()))

    db.add(invoice)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invoice could not be created — check invoice_no is unique "
            "and client_id exists.",
        ) from exc

    db.refresh(invoice)
    return invoice


@router.get("/{invoice_id}", response_model=schemas.InvoiceRead)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """Fetch a single invoice by id (included for convenience when
    testing/using update & delete)."""
    return _get_invoice_or_404(db, invoice_id)


@router.put("/{invoice_id}", response_model=schemas.InvoiceRead)
def update_invoice(
    invoice_id: int,
    payload: schemas.InvoiceUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing invoice.

    Only fields explicitly set on the request body are updated
    (partial update semantics, safe for use as PUT or PATCH).

    If `products` is included in the payload, the invoice's existing
    line items are fully replaced with the ones provided — thanks to
    `cascade="all, delete-orphan"` on the relationship, the old rows
    are cleaned up automatically.
    """
    invoice = _get_invoice_or_404(db, invoice_id)

    update_data = payload.model_dump(exclude_unset=True, exclude={"products"})
    for field, value in update_data.items():
        setattr(invoice, field, value)

    if payload.products is not None:
        invoice.products.clear()
        for product in payload.products:
            invoice.products.append(models.ProductItems(**product.model_dump()))

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invoice could not be updated — check invoice_no is unique "
            "and client_id exists.",
        ) from exc

    db.refresh(invoice)
    return invoice


@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """Delete an invoice. Associated product line items are removed
    automatically via the cascade configured on the relationship."""
    invoice = _get_invoice_or_404(db, invoice_id)
    db.delete(invoice)
    db.commit()
    return None
