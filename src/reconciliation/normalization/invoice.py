from ..models.invoice import Invoice
from .common import safe_float


def normalize_invoice(row: dict) -> Invoice:
    return Invoice(
        invoice_number=row["invoice_number"].strip(),
        invoice_date=row["invoice_date"].strip(),
        vendor_id=row["vendor_id"].strip(),
        vendor_name_on_invoice=row["vendor_name_on_invoice"].strip(),
        po_number=row["po_number"].strip(),
        sku=row["sku"].strip(),
        uom=row["uom"].strip(),
        qty=safe_float(row["qty"]),
        rate=safe_float(row["rate"]),
        taxable_value=safe_float(row["taxable_value"]),
        gst_rate_pct=safe_float(row["gst_rate_pct"]),
        gst_amount=safe_float(row["gst_amount"]),
        invoice_total=safe_float(row["invoice_total"]),
    )
