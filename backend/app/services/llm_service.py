import os
import json
import google.generativeai as genai
from typing import Dict, Any

# Ensure you have GEMINI_API_KEY set in your environment
api_key = os.getenv("GEMINI_API_KEY")
if api_key and api_key != "your-key-here":
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
        import random
        # Fallback for testing without API key
        try:
            history = json.loads(short_history)
            turn_number = len(history)
        except:
            turn_number = 0
            
        mock_actions = ["FOLLOW_UP", "FOLLOW_UP", "GO_DEEPER", "CHANGE_TOPIC"]
        mock_action = mock_actions[turn_number % len(mock_actions)]
        
        topic_title = current_day.get('title')
        # Extract just the job title from "Role: Senior Data Engineer"
        job_role = candidate_summary.replace("Role: ", "")
        
        if mock_action == "CHANGE_TOPIC":
            next_q = random.choice([
                f"That makes sense. Let's shift gears. As a {job_role}, how would you approach the next topic?",
                f"Good answer. Let's move on to the next subject now. How does a {job_role} handle...",
                f"I understand your point. Let's explore a completely different area now."
            ])
        elif mock_action == "GO_DEEPER":
            next_q = random.choice([
                f"Interesting. How would you apply the concepts of {topic_title} in a real production environment as a {job_role}?",
                f"Can you elaborate on the potential challenges a {job_role} might face when deploying {topic_title} at scale?",
                f"That's a good summary. What are the engineering trade-offs when implementing {topic_title} on your team?"
            ])
        else:
            next_q = random.choice([
                f"Can you explain a bit more about how {topic_title} works under the hood from a {job_role}'s perspective?",
                f"Could you dive a little deeper into the technical details of {topic_title}?",
                f"What specifically makes {topic_title} so important for a {job_role} in this architecture?"
            ])
            
        return {
            "accuracy": "partial",
            "strengths": ["Attempted to answer"],
            "missing_concepts": ["Missing depth"],
            "misconceptions": [],
            "next_action": mock_action,
            "reason_short": "Mock evaluation fallback",
            "next_question": next_q
        }

    current_day_title = current_day.get('title')
    current_day_objectives = json.dumps(current_day.get('objectives', []))

    prompt = f"""
    You are a professional technical interviewer for the ABTalks AI Cohort.
    Candidate Summary: {candidate_summary}
    Topic Day: {current_day_title}
    Topic Objectives: {current_day_objectives}

    Previous Question: {previous_question}
    Candidate Answer: {candidate_answer}
    Interview History: {short_history}
    Allowed Next Actions: {allowed_next_actions}

    Evaluate the candidate's answer and decide the next action. Then generate the next question.
    CRITICAL: You MUST tailor your generated question specifically to the candidate's job role ({candidate_summary}). For example, if they are a Data Engineer, ask how they would build data pipelines for this topic.
    Ground your questions STRICTLY in the supplied curriculum day and objectives.
    Return ONLY a valid JSON object matching this exact schema:
    {{
      "accuracy": "strong | partial | weak",
      "strengths": ["..."],
      "missing_concepts": ["..."],
      "misconceptions": ["..."],
      "next_action": "one of the Allowed Next Actions",
      "reason_short": "one sentence explaining the decision",
      "next_question": "the actual next question to ask the candidate, tailored to their Job Role"
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
