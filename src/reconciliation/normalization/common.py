def normalize_id(value: str) -> str:
    """Trim and uppercase an identifier for comparison purposes only --
    never used for output, since the submission must echo the original
    invoice_number verbatim."""
    return (value or "").strip().upper()


def safe_float(value, default=0.0):
    """Parse a field as float. Handles both a CSV string ('176') and a
    native JSON number (176, 176.0) -- this module was written for CSV
    rows only, but the sandbox API returns real ints/floats for the same
    fields (confirmed: /erp/invoices' qty is a JSON int, not a string),
    and calling .strip() on a non-string used to raise AttributeError.
    Blank/None fields (e.g. list_price_2019 for a product with no 2019
    price) should stay a real None, not 0.0 -- caller picks the right
    default for the field."""
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return float(value)
    value = value.strip()
    if value == "":
        return default
    try:
        return float(value)
    except ValueError:
        return default
