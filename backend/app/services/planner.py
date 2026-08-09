import random
from app.models.session import CandidateAnalysis
from app.services.curriculum_service import get_day

def get_module_for_day(day_number: int) -> int:
    if 1 <= day_number <= 3: return 1
    if 4 <= day_number <= 6: return 2
    if 7 <= day_number <= 10: return 3
    if 11 <= day_number <= 15: return 4
    if 16 <= day_number <= 20: return 5
    if 21 <= day_number <= 24: return 6
    if 25 <= day_number <= 28: return 7
    if 29 <= day_number <= 31: return 8
    return 0

def build_plan(analysis: CandidateAnalysis) -> list[int]:
    """Select 5 diverse completed days for the interview plan."""
    eligible_days = analysis.passed_days
    if not eligible_days:
        return []
    
    scored_days = []
    selected_modules = set()
    
    for day_num in eligible_days:
        day_data = get_day(day_num)
        if not day_data:
            continue
            
        score = 10  # base weight
        
        # verification bonus for struggling concepts
        attempts = analysis.attempt_counts.get(day_num, 0)
        if attempts >= 3:
            score += 5
            
        # engineering bonus
        day_type = day_data.get("type", "")
        if day_type in ["SHIP_IT", "CAPSTONE"]:
            score += 5
            
        # Add to scored list
        scored_days.append((score, day_num, get_module_for_day(day_num)))
        
    # Sort by score descending
    scored_days.sort(key=lambda x: x[0], reverse=True)
    
    final_plan = []
    
    # Try to pick 5 days, prioritizing diversity
    for score, day_num, mod in scored_days:
        if len(final_plan) >= 5:
            break
        if mod not in selected_modules:
            final_plan.append(day_num)
            selected_modules.add(mod)
            
    # If we still need more days to reach 5, pick remaining highest scored days
    for score, day_num, mod in scored_days:
        if len(final_plan) >= 5:
            break
        if day_num not in final_plan:
            final_plan.append(day_num)
            
    # Shuffle the plan to make the interview feel natural
    random.shuffle(final_plan)
    
    return final_plan
