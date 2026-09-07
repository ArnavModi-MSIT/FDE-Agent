from dataclasses import dataclass


@dataclass(frozen=True)
class Vendor:
    vendor_id: str
    vendor_name: str
    gstin: str
    city: str
    state: str
    payment_terms_days: int
    msme_registered: str
    source_system: str
