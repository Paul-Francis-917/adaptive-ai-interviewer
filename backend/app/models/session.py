from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any

class MemberInfo(BaseModel):
    id: str
    name: str
    jobRole: str
    yearsExperience: int
    education: str
    status: str

class MissionRecord(BaseModel):
    day: int
    title: str
    passed: Optional[bool] = None
    skipped: Optional[bool] = None
    attempts: Optional[int] = 0

class LearningSignals(BaseModel):
    commitDays: int
    missionsCompleted: int
    missionsFirstTry: int

class CandidateProfile(BaseModel):
    member: MemberInfo
    missions: List[MissionRecord]
    signals: LearningSignals

class CandidateAnalysis(BaseModel):
    candidate: CandidateProfile
    passed_days: List[int]
    failed_days: List[int]
    skipped_days: List[int]
    attempt_counts: Dict[int, int]  # day -> attempts

class TurnRecord(BaseModel):
    day: int
    question: str
    answer: str
    evaluation_summary: str
    next_action: str

class InterviewSession(BaseModel):
    session_id: str
    candidate: CandidateProfile
    plan: List[int]
    current_day: int
    question_count: int = 0
    days_covered: List[int] = []
    difficulty: str = "intermediate"
    history: List[TurnRecord] = []
    current_question: str = ""
