from dataclasses import dataclass
from typing import Optional

from .registry import parse_uom


@dataclass(frozen=True)
class CanonicalQuantity:
    ok: bool
    base_unit: Optional[str]
    canonical_qty: Optional[float]
    canonical_rate: Optional[float]  # rate per base unit, not per package


def canonicalize(qty: float, rate: float, uom: str) -> CanonicalQuantity:
    """Convert a (qty, rate, uom) triple to a common base unit so that a
    quantity/rate billed 'per box' can be compared against one billed 'per
    unit'. Confirmed necessary against real data: a Box(10) invoice's raw
    rate is exactly 10x its PO's per-unit rate -- comparing raw rates
    without this would falsely flag RATE_MISMATCH alongside UOM_MISMATCH."""
    parsed = parse_uom(uom)
    if parsed is None:
        return CanonicalQuantity(ok=False, base_unit=None, canonical_qty=None, canonical_rate=None)
    base_unit, multiplier = parsed
    return CanonicalQuantity(
        ok=True,
        base_unit=base_unit,
        canonical_qty=qty * multiplier,
        canonical_rate=rate / multiplier,
    )
