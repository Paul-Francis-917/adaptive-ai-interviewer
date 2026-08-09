import json
import os
from pathlib import Path

# Load curriculum once at module level to keep it in memory
_curriculum_by_day = {}

def load_curriculum():
    global _curriculum_by_day
    data_path = Path(__file__).parent.parent.parent / "data" / "curriculum.json"
    if not data_path.exists():
        # Fallback empty or default for testing if not found
        _curriculum_by_day = {}
        return
        
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for day in data:
            _curriculum_by_day[day["day"]] = day

def get_day(day_number: int) -> dict:
    if not _curriculum_by_day:
        load_curriculum()
    return _curriculum_by_day.get(day_number)

def get_all_days() -> list:
    if not _curriculum_by_day:
        load_curriculum()
    return list(_curriculum_by_day.values())

# Initialize on import
load_curriculum()
