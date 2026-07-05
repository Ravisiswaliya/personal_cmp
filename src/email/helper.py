from pathlib import Path

from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).resolve().parent

env = Environment(loader=FileSystemLoader(BASE_DIR / "templates"))


def render_template(template_name: str, context: dict) -> str:
    template = env.get_template(template_name)
    print(template, "+++++++template")
    return template.render(**context)


html = render_template(
    "invoice.html",
    {
        "customer_name": "John Doe",
        "invoice_number": "INV-1001",
        "invoice_date": "05 Jul 2026",
        "due_date": "15 Jul 2026",
        "currency": "₹",
        "amount": "15,000",
        "company_name": "ABC Technologies",
        "sender_name": "Ravi Siswaliya",
    },
)
