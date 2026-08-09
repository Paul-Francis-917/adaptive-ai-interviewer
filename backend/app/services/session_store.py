from typing import Dict, Optional
from app.models.session import InterviewSession

# In-memory dictionary for hackathon MVP
_sessions: Dict[str, InterviewSession] = {}

def create_session(session: InterviewSession) -> None:
    _sessions[session.session_id] = session

def get_session(session_id: str) -> Optional[InterviewSession]:
    return _sessions.get(session_id)

def update_session(session: InterviewSession) -> None:
    _sessions[session.session_id] = session

def delete_session(session_id: str) -> None:
    if session_id in _sessions:
        del _sessions[session_id]
