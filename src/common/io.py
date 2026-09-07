import csv


def read_csv_rows(path: str) -> list[dict]:
    """Read a CSV into a list of plain dicts. Every reconciliation source
    file is small enough to hold fully in memory; no streaming needed."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
