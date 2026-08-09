import json
import os
import google.generativeai as genai
from typing import Dict, Any

from app.models.session import InterviewSession, TurnRecord, CandidateProfile, CandidateAnalysis
from app.services.curriculum_service import get_day
from app.services.planner import build_plan
from app.services.profile_service import analyze_candidate
from app.services.llm_service import generate_first_question, evaluate_and_generate_next, LLMOutput

API_KEY = os.getenv("GEMINI_API_KEY")

def initialize_interview(session: InterviewSession) -> str:
    """Analyze profile, build plan, and generate first question."""
    analysis = analyze_candidate(session.candidate)
    plan = build_plan(analysis)
    
    # fallback if plan empty
    if not plan:
        plan = [1, 2, 3, 4, 5]
        
    session.plan = plan
    session.current_day = plan[0]
    session.days_covered = [plan[0]]
    session.question_count = 1
    
    day_data = get_day(session.current_day)
    candidate_summary = session.candidate.member.dict()
    
    first_question = generate_first_question(candidate_summary, day_data)
    session.current_question = first_question
    return first_question

def process_turn(session: InterviewSession, candidate_message: str) -> Dict[str, Any]:
    day_data = get_day(session.current_day)
    candidate_summary = session.candidate.member.dict()
    
    coverage_status = f"Questions asked: {session.question_count}/8 minimum. Days covered: {len(set(session.days_covered))}/4 minimum."
    
    evaluation = evaluate_and_generate_next(
        candidate_summary,
        day_data,
        session.current_question,
        candidate_message,
        coverage_status
    )
    
    # Store turn history
    turn = TurnRecord(
        day=session.current_day,
        question=session.current_question,
        answer=candidate_message,
        evaluation_summary=evaluation.reason_short,
        next_action=evaluation.next_action
    )
    session.history.append(turn)
    
    # Coverage Guard Logic
    can_finish = session.question_count >= 8 and len(set(session.days_covered)) >= 4
    
    days_needed = 4 - len(set(session.days_covered))
    questions_remaining = max(0, 8 - session.question_count)
    
    force_new_day = False
    if not can_finish:
        # If we barely have enough questions left to cover the needed days, force a new day
        if questions_remaining <= days_needed:
            force_new_day = True
            
    next_action = evaluation.next_action
    if force_new_day:
        next_action = "CHANGE_TOPIC"
        
    # Apply action
    if next_action == "CHANGE_TOPIC":
        # Find next uncovered planned day
        uncovered_days = [d for d in session.plan if d not in session.days_covered]
        if uncovered_days:
            session.current_day = uncovered_days[0]
            session.days_covered.append(session.current_day)
        else:
            # If all planned days covered, just loop or pick random
            pass
            
    # Update question count
    session.question_count += 1
    session.current_question = evaluation.next_question
    
    # Check if we should finish
    if can_finish and next_action == "CHANGE_TOPIC":
        # Time to wrap up
        return {
            "reply": "Interview completed.",
            "done": True,
            "feedback": generate_final_feedback(session)
        }
        
    return {
        "reply": session.current_question,
        "done": False
    }

def generate_final_feedback(session: InterviewSession) -> dict:
    if not API_KEY:
        return {
            "summary": "This was a mock interview since no API key was provided.",
            "strengths": ["Mock strength"],
            "gaps": ["Mock gap"],
            "next": ["Review mock topic"]
        }
        
    prompt = f"""
    Based on the following interview history, generate a final feedback report.
    Candidate: {session.candidate.member.name}
    
    History:
    """
    for turn in session.history:
        prompt += f"Q: {turn.question}\nA: {turn.answer}\nEval: {turn.evaluation_summary}\n\n"
        
    prompt += """
    Output MUST be a JSON object with exactly these keys:
    - summary: 2-4 sentences describing overall interview performance
    - strengths: array of strings describing specific demonstrated strengths
    - gaps: array of strings describing specific missing concepts or misconceptions
    - next: array of strings with concrete next steps tied back to curriculum days
    """
    
    model = genai.GenerativeModel('gemini-1.5-pro', system_instruction="You are a professional technical interviewer providing structured feedback.")
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json"
        )
    )
    
    try:
        return json.loads(response.text)
    except:
        return {
            "summary": "Error parsing LLM feedback.",
            "strengths": [],
            "gaps": [],
            "next": []
        }
