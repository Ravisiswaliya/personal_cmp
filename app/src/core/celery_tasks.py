import time

from app.src.core.celery_app import celery


@celery.task(
    retry_backoff=True,
)
def add(x: int, y: int):
    print(f"Adding {x} + {y} ")
    time.sleep(5)
    res = x + y
    print(f"Added result: {res} ")
    return res


@celery.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    retry_kwargs={"max_retries": 5},
)
def process_monthly_invoice_report(self, invoice_month: int):
    # Perform your business logic here
    return f"Processed order {invoice_month}"
