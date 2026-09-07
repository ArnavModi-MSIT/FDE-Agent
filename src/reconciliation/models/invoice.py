from dataclasses import dataclass


@dataclass(frozen=True)
class Invoice:
    invoice_number: str
    invoice_date: str
    vendor_id: str
    vendor_name_on_invoice: str
    po_number: str
    sku: str
    uom: str
    qty: float
    rate: float
    taxable_value: float
    gst_rate_pct: float
    gst_amount: float
    invoice_total: float
