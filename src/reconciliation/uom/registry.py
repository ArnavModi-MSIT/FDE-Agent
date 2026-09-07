import re
from typing import Optional, Tuple

BASE_UNIT = "Nos"

# Matches a packaging notation like "Box(10)" or "Carton(20)" -- any label
# followed by a parenthesized count. Confirmed real: vendor_invoices.csv has
# 13 rows billed as "Box(10)" against POs that are always plain "Nos".
_PACKAGED_UOM_PATTERN = re.compile(r"^(?P<label>[A-Za-z]+)\((?P<count>\d+)\)$")


def parse_uom(uom: str) -> Optional[Tuple[str, float]]:
    """Return (base_unit, multiplier) for a uom string, or None if it can't
    be resolved. Never guesses at an unrecognized unit -- an unresolvable
    uom must surface as UOM_MISMATCH, not a silently wrong conversion."""
    uom = (uom or "").strip()
    if uom == BASE_UNIT:
        return BASE_UNIT, 1.0
    match = _PACKAGED_UOM_PATTERN.match(uom)
    if match:
        count = int(match.group("count"))
        if count <= 0:
            return None
        return BASE_UNIT, float(count)
    return None
