from typing import Dict, List

from ..models.vendor import Vendor


def build_vendor_gstin_index(vendors: List[Vendor]) -> Dict[str, str]:
    """vendor_id -> gstin, so checks/vendor.py can resolve two different
    vendor codes that both file the same GSTIN (a real duplicate-vendor
    pattern confirmed in vendors.csv, not a hypothetical one)."""
    return {v.vendor_id: v.gstin for v in vendors}
