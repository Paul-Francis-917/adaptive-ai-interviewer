import os
import json
import google.generativeai as genai
from typing import Dict, Any

# Ensure you have GEMINI_API_KEY set in your environment
api_key = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6ID1lWMix2QneTFaJ5ThBiznaCBV9FCkeMjpHPNcuU93Q")
if api_key:
    genai.configure(api_key=api_key)

# We'll use a model that supports structured JSON output.
MODEL_NAME = "gemini-1.5-flash"

def evaluate_answer_and_generate_next(
    candidate_summary: str,
    current_day: Dict[str, Any],
    difficulty: str,
    previous_question: str,
    candidate_answer: str,
    short_history: str,
    allowed_next_actions: str
) -> Dict[str, Any]:
    """
    Calls the LLM to evaluate the answer, decide the next action, and generate the next question.
    """
    if not api_key:
        # Fallback for testing without API key
        return {
            "accuracy": "partial",
            "strengths": ["Attempted to answer"],
            "missing_concepts": ["Missing depth"],
            "misconceptions": [],
            "next_action": "FOLLOW_UP",
            "reason_short": "Mock evaluation fallback",
            "next_question": f"Can you explain more about {current_day.get('title')}?"
        }

    prompt = f"""
    You are a professional technical interviewer.
    Candidate Summary: {candidate_summary}
    Topic Day: {current_day.get('title')}
    Topic Objectives: {json.dumps(current_day.get('objectives', []))}
    Current Difficulty: {difficulty}
    
    Previous Question: {previous_question}
    Candidate Answer: {candidate_answer}
    
    Interview History:
    {short_history}
    
    Allowed Next Actions: {allowed_next_actions}
    
    Evaluate the candidate's answer and decide the next action. Then generate the next question.
    Return ONLY a valid JSON object matching this exact schema:
    {{
      "accuracy": "strong | partial | weak",
      "strengths": ["..."],
      "missing_concepts": ["..."],
      "misconceptions": ["..."],
      "next_action": "one of the Allowed Next Actions",
      "reason_short": "one sentence explaining the decision",
      "next_question": "the actual next question to ask the candidate"
    }}
    """
    
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        # Using response_mime_type to enforce JSON from Gemini 1.5
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"LLM Error: {e}")
        # Safe fallback
        return {
            "accuracy": "partial",
            "strengths": [],
            "missing_concepts": [],
            "misconceptions": [],
            "next_action": "CHANGE_TOPIC",
            "reason_short": "Error connecting to LLM",
            "next_question": "Let's move on to the next topic."
        }

def generate_first_question(day: Dict[str, Any]) -> str:
    if not api_key:
        return f"To start, can you explain what you learned about {day.get('title')}?"
        
    prompt = f"""
    You are a professional technical interviewer.
    Start the interview by asking a fundamental question about the following topic.
    Topic: {day.get('title')}
    Objectives: {json.dumps(day.get('objectives', []))}
    
    Return ONLY the question text.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Let's begin by discussing {day.get('title')}. What can you tell me about it?"

def generate_final_feedback(history: str) -> Dict[str, Any]:
    """Generates the final summary, strengths, gaps, and next steps."""
    if not api_key:
        return {
            "summary": "Interview completed successfully.",
            "strengths": ["Completed the interview"],
            "gaps": ["No detailed gaps analyzed due to offline mode"],
            "next": ["Review the curriculum again"]
        }
        
    prompt = f"""
    Based on the following interview history, generate a final feedback report.
    History:
    {history}
    
    Return ONLY a valid JSON object matching this schema:
    {{
      "summary": "2-4 sentences describing overall interview performance",
      "strengths": ["Specific demonstrated strength 1", "..."],
      "gaps": ["Specific missing concept 1", "..."],
      "next": ["Concrete next step tied back to curriculum days"]
    }}
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        return json.loads(response.text)
    except Exception as e:
        return {
            "summary": "Error generating feedback.",
            "strengths": [],
            "gaps": [],
            "next": []
        }
