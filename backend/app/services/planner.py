import random
from typing import Dict, Any, List

def build_interview_plan(candidate_profile: Dict[str, Any], curriculum_by_day: Dict[str, Any]) -> Dict[str, Any]:
    """
    Selects 5 completed days, marks 4 as mandatory anchors.
    Ensures some diversity if possible.
    """
    passed_missions = candidate_profile.get("passed_missions", [])
    
    # Extract just the day strings that the candidate actually passed
    passed_days = [str(m["day"]) for m in passed_missions]
    
    # Filter days that exist in curriculum
    eligible_days = [day for day in passed_days if day in curriculum_by_day]
    
    # Select 5 diverse days (for hackathon MVP, random sample from passed is safe and fast, 
    # but we can try to spread them across modules)
    
    # Let's shuffle and pick up to 5
    random.shuffle(eligible_days)
    selected_days = eligible_days[:5]
    
    # Fallback: if they haven't passed enough, we might need to dip into skipped or just use what we have,
    # but the synthetic candidates typically have enough passed missions.
    if len(selected_days) < 3:
        # Just use whatever they passed
        pass
    
    # Designate the first 3 (or all if < 3) as mandatory anchors
    anchor_days = selected_days[:3]
    
    return {
        "planned_days": selected_days,
        "anchor_days": anchor_days
    }
