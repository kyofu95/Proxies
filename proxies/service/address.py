from dataclasses import dataclass
from typing import Optional


@dataclass
class Address:
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
