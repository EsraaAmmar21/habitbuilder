from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class Challenge:
    id: Optional[int]
    name: str
    description: str
    creator_id: int
    start_date: datetime
    end_date: datetime
    participants: List[int] = None
    
    def __post_init__(self):
        if self.participants is None:
            self.participants = []