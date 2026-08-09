import os
import json
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List, Optional

from app.prompts.prompts import SYSTEM_PROMPT, FIRST_QUESTION_PROMPT, EVALUATION_AND_NEXT_PROMPT

class LLMOutput(BaseModel):
    accuracy: str = Field(description="strong | partial | weak")
    strengths: List[str] = Field(description="Specific strengths demonstrated")
    missing_concepts: List[str] = Field(description="Missing concepts")
    misconceptions: List[str] = Field(description="Misconceptions")
    next_action: str = Field(description="FOLLOW_UP | GO_DEEPER | SIMPLIFY | CHANGE_TOPIC")
    reason_short: str = Field(description="One sentence for logs, not chain-of-thought")
    next_question: str = Field(description="The actual next question to ask the candidate")

# Initialize Gemini if key exists
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

def generate_first_question(candidate_summary: dict, day_data: dict) -> str:
    if not API_KEY:
        return f"Welcome! Let's start with {day_data.get('title')}. Can you explain the basics?"
        
    model = genai.GenerativeModel('gemini-1.5-pro', system_instruction=SYSTEM_PROMPT)
    prompt = FIRST_QUESTION_PROMPT.format(
        candidate_name=candidate_summary.get("name"),
        job_role=candidate_summary.get("jobRole"),
        experience=candidate_summary.get("yearsExperience"),
        day_title=day_data.get("title"),
        objectives=", ".join(day_data.get("objectives", []))
    )
    
    response = model.generate_content(prompt)
    return response.text.strip()

def evaluate_and_generate_next(
    candidate_summary: dict, 
    day_data: dict, 
    previous_question: str, 
    candidate_answer: str,
    coverage_status: str
) -> LLMOutput:
    if not API_KEY:
        return LLMOutput(
            accuracy="partial",
            strengths=["Answered in mock mode"],
            missing_concepts=["Mock missing concept"],
            misconceptions=[],
            next_action="CHANGE_TOPIC",
            reason_short="Mocking next action",
            next_question="This is a mock follow-up question."
        )
        
    model = genai.GenerativeModel('gemini-1.5-pro', system_instruction=SYSTEM_PROMPT)
    
    prompt = EVALUATION_AND_NEXT_PROMPT.format(
        candidate_name=candidate_summary.get("name"),
        job_role=candidate_summary.get("jobRole"),
        day_title=day_data.get("title"),
        objectives=", ".join(day_data.get("objectives", [])),
        previous_question=previous_question,
        candidate_answer=candidate_answer,
        coverage_status=coverage_status
    )
    
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=LLMOutput
        )
    )
    
    try:
        data = json.loads(response.text)
        return LLMOutput(**data)
    except Exception as e:
        # Fallback in case of parse error
        return LLMOutput(
            accuracy="partial",
            strengths=[],
            missing_concepts=[],
            misconceptions=[],
            next_action="CHANGE_TOPIC",
            reason_short=str(e),
            next_question="I didn't quite catch that. Could you explain it differently?"
        )
