from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from app.services.session_store import create_session, get_session
from app.services.profile_service import analyze_candidate
from app.services.curriculum_service import CURRICULUM_BY_DAY
from app.services.planner import build_interview_plan
from app.services.llm_service import generate_first_question
from app.services.interview_engine import process_turn

router = APIRouter()

class StartInterviewRequest(BaseModel):
    sessionId: str
    candidate: Dict[str, Any]

class ContinueInterviewRequest(BaseModel):
    sessionId: str
    message: str

class InterviewRequest(BaseModel):
    sessionId: str
    candidate: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

class Feedback(BaseModel):
    summary: str
    strengths: List[str]
    gaps: List[str]
    next: List[str]

class InterviewResponse(BaseModel):
    reply: str
    done: bool
    feedback: Optional[Feedback] = None

@router.post("/interview", response_model=InterviewResponse)
def handle_interview(req: InterviewRequest):
    if not req.sessionId:
        raise HTTPException(status_code=400, detail="sessionId is required")

    # Start Interview branch
    if req.candidate:
        profile = analyze_candidate(req.candidate)
        plan = build_interview_plan(profile, CURRICULUM_BY_DAY)
        session = create_session(req.sessionId, req.candidate, plan)
        
        # We need a first question
        day_num = session["current_day"]
        day_data = CURRICULUM_BY_DAY.get(day_num, {})
        first_q = generate_first_question(day_data)
        
        # Save first question as a placeholder in session so we have context for the next answer
        session["first_question"] = first_q
        
        return InterviewResponse(
            reply=first_q,
            done=False
        )

    # Continue Interview branch
    elif req.message:
        try:
            result = process_turn(req.sessionId, req.message)
            return InterviewResponse(**result)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
            
    else:
        raise HTTPException(status_code=400, detail="Must provide candidate or message")
