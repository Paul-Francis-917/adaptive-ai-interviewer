from typing import Dict, Any, List

# In-memory session store for hackathon MVP
SESSIONS: Dict[str, Dict[str, Any]] = {}

def create_session(session_id: str, candidate_data: Dict[str, Any], plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Initializes a new interview session.
    """
    session = {
        "session_id": session_id,
        "candidate": candidate_data,
        "plan": plan,
        "current_day": plan["planned_days"][0] if plan.get("planned_days") else None,
        "question_count": 0,
        "days_covered": [],
        "difficulty": "intermediate",
        "history": [],
        "is_completed": False
    }
    SESSIONS[session_id] = session
    return session

def get_session(session_id: str) -> Dict[str, Any]:
    """
    Retrieves an existing session.
    """
    return SESSIONS.get(session_id)

def update_session(session_id: str, updates: Dict[str, Any]) -> None:
    """
    Updates the session with new values (e.g. tracking questions asked, history).
    """
    if session_id in SESSIONS:
        SESSIONS[session_id].update(updates)

def save_turn_history(session_id: str, day: str, question: str, answer: str, evaluation_summary: str, next_action: str) -> None:
    """
    Appends a turn to the session history.
    """
    if session_id in SESSIONS:
        SESSIONS[session_id]["history"].append({
            "day": day,
            "question": question,
            "answer": answer,
            "evaluation_summary": evaluation_summary,
            "next_action": next_action
        })
        
        # Track coverage
        if day not in SESSIONS[session_id]["days_covered"]:
            SESSIONS[session_id]["days_covered"].append(day)
