"""Run the pool-service data cleanup and sales report."""

import csv
from pathlib import Path

from pipeline.validator import inspect_rows
from pipeline.reporter import form_dashboard, show_dashboard


def read_service_file():
    """Load the service list from the CSV file into Python dictionaries."""
    location = Path(__file__).parent / "data" / "service_visits.csv"

    with open(location, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def start():
    """Bring together the different steps of the project."""
    entries = read_service_file()
    good_entries, rejected_entries = inspect_rows(entries)
    dashboard = form_dashboard(entries, good_entries, rejected_entries)
    show_dashboard(dashboard)


if __name__ == "__main__":
    start()
