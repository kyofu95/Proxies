from dataclasses import dataclass
from typing import Optional


@dataclass
class Address:
    """Represents an address with city, region, and country information."""

    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
