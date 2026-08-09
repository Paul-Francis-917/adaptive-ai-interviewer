import json
import os
from typing import Dict, Any, List

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
CANDIDATES_PATH = os.path.join(DATA_DIR, "candidates.json")

def load_candidates(file_path: str = CANDIDATES_PATH) -> Dict[str, Any]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Build lookup by candidate ID
        candidates_by_id = {}
        for c in data.get("candidates", []):
            candidate_id = c.get("member", {}).get("id")
            if candidate_id:
                candidates_by_id[candidate_id] = c
        return candidates_by_id
    except Exception as e:
        print(f"Error loading candidates from {file_path}: {e}")
        return {}

def analyze_candidate(candidate_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parses a single candidate object and categorizes their missions.
    """
    passed_missions = []
    failed_missions = []
    skipped_missions = []
    
    missions = candidate_data.get("missions", [])
    
    for mission in missions:
        day = str(mission.get("day"))
        if mission.get("skipped") is True:
            skipped_missions.append({
                "day": day,
                "title": mission.get("title")
            })
            continue
            
        if mission.get("passed") is True:
            passed_missions.append({
                "day": day,
                "title": mission.get("title"),
                "attempts": mission.get("attempts", 1)
            })
        else:
            failed_missions.append({
                "day": day,
                "title": mission.get("title"),
                "attempts": mission.get("attempts", 1)
            })

    # Sort them by day (assuming days are integers logically)
    passed_missions = sorted(passed_missions, key=lambda x: int(x["day"]))
    
    profile = {
        "member": candidate_data.get("member", {}),
        "signals": candidate_data.get("signals", {}),
        "passed_missions": passed_missions,
        "failed_missions": failed_missions,
        "skipped_missions": skipped_missions
    }
    return profile

CANDIDATES_BY_ID = load_candidates()
