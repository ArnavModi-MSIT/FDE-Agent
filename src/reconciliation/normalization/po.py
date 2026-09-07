from ..models.purchase_order import PurchaseOrder
from .common import safe_float


def normalize_po(row: dict) -> PurchaseOrder:
    return PurchaseOrder(
        po_number=row["po_number"].strip(),
        po_date=row["po_date"].strip(),
        vendor_id=row["vendor_id"].strip(),
        sku=row["sku"].strip(),
        description=row["description"].strip(),
        uom=row["uom"].strip(),
        qty=safe_float(row["qty"]),
        rate=safe_float(row["rate"]),
        po_value=safe_float(row["po_value"]),
        plant=row["plant"].strip(),
    )
