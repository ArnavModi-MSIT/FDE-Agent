from dataclasses import dataclass
from typing import Dict, Optional

from ..models.invoice import Invoice
from ..models.purchase_order import PurchaseOrder
from . import exact, fuzzy


@dataclass(frozen=True)
class MatchResult:
    matched: bool
    purchase_order: Optional[PurchaseOrder]
    match_type: str  # "exact" | "normalized" | "none"


def resolve(
    invoice: Invoice,
    po_index: Dict[str, PurchaseOrder],
    normalized_po_index: Dict[str, PurchaseOrder],
) -> MatchResult:
    po = exact.match_exact(invoice, po_index)
    if po is not None:
        return MatchResult(True, po, "exact")

    po = fuzzy.match_normalized(invoice, normalized_po_index)
    if po is not None:
        return MatchResult(True, po, "normalized")

    return MatchResult(False, None, "none")
