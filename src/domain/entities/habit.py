from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Habit:
    id: Optional[int]
    user_id: int
    name: str
    description: str
    frequency: str  # daily, weekly, monthly
    streak: int
    created_at: datetime
    reminder_time: Optional[datetime]
    last_completed: Optional[datetime]