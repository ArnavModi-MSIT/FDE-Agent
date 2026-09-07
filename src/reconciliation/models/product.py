from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Product:
    sku: str
    description: str
    family: str
    uom: str
    list_price_2019: Optional[float]
    list_price_2023: Optional[float]
