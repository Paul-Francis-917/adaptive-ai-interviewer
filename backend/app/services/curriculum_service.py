import json
import os
from typing import Dict, Any

# Adjust path based on where the app runs from
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
CURRICULUM_PATH = os.path.join(DATA_DIR, "curriculum.json")

def load_curriculum(file_path: str = CURRICULUM_PATH) -> Dict[str, Any]:
    """
    Loads the curriculum JSON and builds a lookup dictionary
    keyed by the day number.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        curriculum_by_day = {}
        for module in data.get("modules", []):
            for day in module.get("days", []):
                day_num = str(day.get("day"))
                curriculum_by_day[day_num] = {
                    "title": day.get("title", ""),
                    "type": day.get("type", ""),
                    "tools": day.get("tools", []),
                    "objectives": day.get("objectives", []),
                    "module": module.get("module_title", "")
                }
        return curriculum_by_day
    except Exception as e:
        print(f"Error loading curriculum from {file_path}: {e}")
        return {}

# Load on startup to keep it in memory
CURRICULUM_BY_DAY = load_curriculum()
