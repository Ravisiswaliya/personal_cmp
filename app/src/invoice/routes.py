# Method    # Path                  # Behavior
# POST      /invoices               # Creates invoice + nested product line items in one call
# GET       /invoices/{invoice_id}  # Fetch one (included for convenience so you can test update/delete)
# PUT       /invoices/{invoice_id}  # Partial update — only fields you send are changed
# DELETE    /invoices/{invoice_id}  # Deletes invoice; products cascade-delete automatically
