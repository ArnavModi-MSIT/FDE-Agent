from ..models.vendor import Vendor
from .common import safe_float


def normalize_vendor(row: dict) -> Vendor:
    """Not yet consumed by any check -- vendor_id equality (checks/vendor.py)
    is sufficient for the reconciliation family today. Present so the vendor
    master is ready to load once a check needs it (e.g. MSME/GSTIN
    validation), per the modular layout, not because it's wired in yet."""
    return Vendor(
        vendor_id=row["vendor_id"].strip(),
        vendor_name=row["vendor_name"].strip(),
        gstin=row["gstin"].strip(),
        city=row["city"].strip(),
        state=row["state"].strip(),
        payment_terms_days=int(safe_float(row["payment_terms_days"])),
        msme_registered=row["msme_registered"].strip(),
        source_system=row["source_system"].strip(),
    )
