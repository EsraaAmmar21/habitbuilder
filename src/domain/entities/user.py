from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class User:
    id: Optional[int]
    username: str
    email: str
    password_hash: str
    created_at: datetime
    goals: List[str] = None
    
    def __post_init__(self):
        if self.goals is None:
            self.goals = []