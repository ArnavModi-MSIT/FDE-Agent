from dataclasses import dataclass


@dataclass(frozen=True)
class PurchaseOrder:
    po_number: str
    po_date: str
    vendor_id: str
    sku: str
    description: str
    uom: str
    qty: float
    rate: float
    po_value: float
    plant: str
