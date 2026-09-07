from typing import Dict, List, Optional

from ..models.invoice import Invoice
from ..models.purchase_order import PurchaseOrder


def build_po_index(purchase_orders: List[PurchaseOrder]) -> Dict[str, PurchaseOrder]:
    return {po.po_number: po for po in purchase_orders}


def match_exact(invoice: Invoice, po_index: Dict[str, PurchaseOrder]) -> Optional[PurchaseOrder]:
    return po_index.get(invoice.po_number)
