def normalize_id(value: str) -> str:
    """Trim and uppercase an identifier for comparison purposes only --
    never used for output, since the submission must echo the original
    invoice_number verbatim."""
    return (value or "").strip().upper()


def safe_float(value, default=0.0):
    """Parse a CSV field as float. Blank fields (e.g. list_price_2019 for a
    product with no 2019 price) should stay a real None, not 0.0 -- caller
    picks the right default for the field."""
    if value is None:
        return default
    value = value.strip()
    if value == "":
        return default
    try:
        return float(value)
    except ValueError:
        return default
