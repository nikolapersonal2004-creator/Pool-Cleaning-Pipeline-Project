"""Clean CSV text and set aside rows that have problems."""

from datetime import datetime
from math import isfinite

from pipeline.schema import TransactionRecord


# Every pool service branch belongs to one region.
BRANCHES = {
    "LON-ON": "ON",  # London
    "BAR-ON": "ON",  # Barrie
    "KEL-BC": "BC",  # Kelowna
    "RED-AB": "AB",  # Red Deer
}


def read_amount(value, column_name):
    """Turn a price such as '$150.00' into the number 150.0."""
    if value is None or str(value).strip() == "":
        raise ValueError(column_name + " is missing")

    price_text = str(value).strip().replace("$", "").replace(",", "")

    try:
        amount = float(price_text)
    except ValueError:
        raise ValueError(column_name + " must be a number")

    if not isfinite(amount) or amount < 0:
        raise ValueError(column_name + " cannot be negative or invalid")

    return round(amount, 2)


def check_visit(row):
    """Return a clean TransactionRecord, or explain what is incorrect."""
    branch = str(row.get("branch_id") or "").strip().upper()
    region = str(row.get("province") or "").strip().upper()

    if not branch:
        raise ValueError("branch ID is missing")
    if branch not in BRANCHES:
        raise ValueError("unknown branch: " + branch)
    if region != BRANCHES[branch]:
        raise ValueError("province does not match the branch")

    # Accept either dashes or slashes in the date.
    date_text = str(row.get("transaction_date") or "").strip()
    date_text = date_text.replace("/", "-")
    try:
        visit_date = datetime.strptime(date_text, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("invalid service date")

    tier = str(row.get("customer_tier") or "").strip().title()
    if tier not in ("Basic", "Plus", "Commercial"):
        raise ValueError("customer tier must be Basic, Plus, or Commercial")

    # Each row represents a job with one or more services.
    try:
        quantity = int(str(row.get("item_count") or "").strip())
    except ValueError:
        raise ValueError("item count must be a whole number")
    if quantity < 1:
        raise ValueError("item count must be at least 1")

    charge = read_amount(row.get("revenue"), "revenue")
    expense = read_amount(row.get("cost"), "cost")

    status = str(row.get("status") or "").strip().lower()
    if status not in ("completed", "cancelled"):
        raise ValueError("status must be completed or cancelled")

    # Cancelled jobs are kept as clean records, but are not counted as sales.
    return TransactionRecord(
        branch, visit_date, tier, quantity,
        charge, expense, region, status == "completed"
    )


def inspect_rows(rows):
    """Check all rows without stopping when one has an error."""
    accepted = []
    rejected = []

    # CSV line 1 has headings, so the first data row is line 2.
    for line_number, row in enumerate(rows, start=2):
        try:
            clean_row = check_visit(row)
            accepted.append(clean_row)
        except ValueError as problem:
            rejected.append("CSV line " + str(line_number) + ": " + str(problem))

    return accepted, rejected
