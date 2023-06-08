from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Health:
    connections: int = 0
    failed_connections: int = 0

    last_tested: Optional[datetime] = None
