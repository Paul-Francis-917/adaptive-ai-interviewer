import json
from typing import Dict, Any

from app.services.session_store import get_session, update_session, save_turn_history
from app.services.llm_service import evaluate_answer_and_generate_next, generate_final_feedback
from app.services.curriculum_service import CURRICULUM_BY_DAY

def check_coverage_guard(session: Dict[str, Any]) -> str:
    """
    Ensures we don't finish before 8 questions and 4 distinct days.
    Returns the next forced action if coverage is at risk.
    """
    question_count = session["question_count"]
    days_covered = len(session["days_covered"])
    
    can_finish = (question_count >= 8) and (days_covered >= 4)
    if can_finish:
        return "CAN_FINISH"
        
    remaining_questions = 8 - question_count
    days_needed = 4 - days_covered
    
    # If we have just enough questions left to cover the required days, force a topic change
    if remaining_questions <= days_needed:
        return "FORCE_UNCOVERED_ANCHOR_DAY"
        
    return "NORMAL"

def get_uncovered_anchor_day(session: Dict[str, Any]) -> str:
    anchors = session["plan"].get("anchor_days", [])
    covered = session.get("days_covered", [])
    for anchor in anchors:
        if anchor not in covered:
            return anchor
    # Fallback to any planned day if anchors are somehow covered but total is < 4
    for day in session["plan"].get("planned_days", []):
        if day not in covered:
            return day
    # Absolute fallback
    return anchors[0] if anchors else "1"

def process_turn(session_id: str, candidate_answer: str) -> Dict[str, Any]:
    session = get_session(session_id)
    if not session:
        raise ValueError("Unknown session")
        
    current_day_num = session["current_day"]
    current_day_data = CURRICULUM_BY_DAY.get(current_day_num, {})
    
    # Get last question
    last_turn = session["history"][-1] if session["history"] else {}
    previous_question = last_turn.get("question") if last_turn else session.get("first_question", "")
    
    # Format history
    history_str = json.dumps([
        {"Q": h["question"], "A": h["answer"]} for h in session["history"]
    ])
    
    # Determine allowed actions
    allowed_actions = "FOLLOW_UP | GO_DEEPER | SIMPLIFY | CHANGE_TOPIC"
    guard_status = check_coverage_guard(session)
    if guard_status == "FORCE_UNCOVERED_ANCHOR_DAY":
        allowed_actions = "CHANGE_TOPIC (MUST CHANGE TOPIC to cover minimum days)"

    # Call LLM
    candidate_summary = f"Role: {session['candidate'].get('jobRole', 'Learner')}"
    
    evaluation = evaluate_answer_and_generate_next(
        candidate_summary=candidate_summary,
        current_day=current_day_data,
        difficulty=session["difficulty"],
        previous_question=previous_question,
        candidate_answer=candidate_answer,
        short_history=history_str,
        allowed_next_actions=allowed_actions
    )
    
    # Save history
    save_turn_history(
        session_id=session_id,
        day=current_day_num,
        question=previous_question,
        answer=candidate_answer,
        evaluation_summary=evaluation.get("reason_short", ""),
        next_action=evaluation.get("next_action", "FOLLOW_UP")
    )
    
    # Update question count
    session["question_count"] += 1
    
    # Handle Next Day logic
    next_question = evaluation.get("next_question", "Can you elaborate?")
    
    if evaluation.get("next_action") == "CHANGE_TOPIC" or guard_status == "FORCE_UNCOVERED_ANCHOR_DAY":
        next_day = get_uncovered_anchor_day(session)
        update_session(session_id, {"current_day": next_day})
    
    # Check if we can finish now that we processed this turn
    if check_coverage_guard(session) == "CAN_FINISH" and session["question_count"] >= 8:
        # Generate feedback
        full_history_str = json.dumps([
            {"day": h["day"], "Q": h["question"], "A": h["answer"], "eval": h["evaluation_summary"]} 
            for h in session["history"]
        ])
        feedback = generate_final_feedback(full_history_str)
        update_session(session_id, {"is_completed": True})
        
        return {
            "reply": "Interview completed.",
            "done": True,
            "feedback": feedback
        }

    return {
        "reply": next_question,
        "done": False
    }
