# Project Development Prompts Log

This document details the exact prompts, system instructions, and design philosophies used to build the **Adaptive AI Interviewer** for the ABTalks 60 Day Challenge. 

The prompts are categorized by architectural layers to provide deep insight into the "Vibe Coding" process and the specific constraints applied to the LLM during development.

---

## 1. Backend Infrastructure & Data Services

### Prompt Objective: Scaffolding the Core State Machine
To build a resilient backend that could manage a complex state machine without a full database, the following prompting strategy was used.

**Prompt Used:**
> "Build a FastAPI backend that reads `curriculum.json` and `candidates.json`. Create a `curriculum_service.py` to parse the 31 days into an in-memory dictionary keyed by day. Create a `profile_service.py` that separates a candidate's passed, skipped, and failed missions. Finally, build an in-memory session manager in `session_store.py` that tracks question count, days covered, and a full conversation history log per `sessionId`. Ensure strict Python typing and Pydantic validation."

**Inner Meaning & Outcome:**
This prompt explicitly forbid the AI from using complex databases (like PostgreSQL or Redis) initially, forcing it to focus on a fast, reliable in-memory architecture (`dict`-based state) suitable for a hackathon MVP.

---

## 2. The Adaptive Engine & Coverage Guardrails

### Prompt Objective: Ensuring Hackathon Compliance
The engine needed to guarantee exactly 12 questions and 3 curriculum days were covered, regardless of how the LLM behaved.

**Prompt Used:**
> "Implement an `interview_engine.py` that intercepts the LLM response. Create a strict `check_coverage_guard` function. The interview MUST NEVER finish before exactly 12 questions are asked (4 questions per topic), and at least 3 distinct curriculum days are covered. If the question count reaches a threshold but days are missing, the engine must override the LLM's chosen action and force a `CHANGE_TOPIC` to an uncovered anchor day."

**Inner Meaning & Outcome:**
AI models are notoriously bad at counting and tracking long-term state across multiple stateless HTTP requests. This prompt solved that by removing the counting responsibility from the LLM entirely and placing it into deterministic, hardcoded Python guardrails.

---

## 3. System Prompts for the AI Model (Gemini 1.5 Flash)

### Prompt Objective: Generating Context-Aware, Role-Specific Questions
This is the actual system prompt injected into the Gemini API to ensure questions are grounded in the curriculum and accurately tailored to the candidate's specific job role.

**Prompt Used (Internal System Prompt):**
```text
You are a professional technical interviewer for the ABTalks AI Cohort.
Candidate Summary: {candidate_summary}
Topic Day: {current_day_title}
Topic Objectives: {current_day_objectives}

Previous Question: {previous_question}
Candidate Answer: {candidate_answer}
Interview History: {short_history}
Allowed Next Actions: {allowed_next_actions}

Evaluate the candidate's answer and decide the next action. Then generate the next question.
CRITICAL: You MUST tailor your generated question specifically to the candidate's job role. For example, if they are a Data Engineer, ask how they would build data pipelines for this topic.
Ground your questions STRICTLY in the supplied curriculum day and objectives.
Return ONLY a valid JSON object matching this exact schema:
{
  "accuracy": "strong | partial | weak",
  "strengths": ["..."],
  "missing_concepts": ["..."],
  "misconceptions": ["..."],
  "next_action": "one of the Allowed Next Actions",
  "reason_short": "one sentence explaining the decision",
  "next_question": "the actual next question to ask the candidate, tailored to their Job Role"
}
```

**Inner Meaning & Outcome:**
By passing `allowed_next_actions` dynamically from the Python engine, the LLM is physically constrained to change topics when the engine demands it. The `CRITICAL` role-tailoring instruction ensures that a Machine Learning Engineer gets vastly different questions than a Data Engineer, even if they are being evaluated on the exact same curriculum day.

---

## 4. Frontend & User Experience (React/Vite)

### Prompt Objective: Building a Premium, Multi-Candidate UI
The goal was to move away from generic chatbots and build a specialized, premium interface with real-time feedback, supporting multiple candidates.

**Prompt Used:**
> "Redesign the React/Vite `App.tsx` using TailwindCSS. Create a unified, elegant Candidate Profile card on the START screen showing Name, Job Role, Experience, and Education. Replace the static text with an animated Curriculum Progress Bar tracking `signals.missionsCompleted` out of 31 total missions. Add a 'Skip Candidate' button and an 'Evaluate Next Candidate' flow to seamlessly switch between multiple candidates. At the end of the interview, display the evaluated feedback alongside the candidate's profile, and include an interactive 5-star User Feedback form for the candidate to rate the engine."

**Inner Meaning & Outcome:**
This prompt instructed the AI to focus heavily on micro-interactions and visual hierarchy. Features like the 'View Evaluation' shortcut for previously evaluated candidates and the dynamic Progress Bar create an incredibly polished, professional hackathon submission that feels like a production-ready SaaS product.

---

## 5. Offline Mock Mode & Dynamic Fallback Logic

### Prompt Objective: Preventing API Loop Failures & Retaining Context
When testing locally without an API key, the system needed to simulate a real LLM while still sounding intelligent.

**Prompt Used:**
> "If the `GEMINI_API_KEY` is not present, do not crash the app. Instead, implement a smart offline mock mode. Mathematically cycle the `next_action` array `['FOLLOW_UP', 'FOLLOW_UP', 'GO_DEEPER', 'CHANGE_TOPIC']` based on the turn number. Crucially, dynamically extract the candidate's `jobRole` and inject it into the offline mock strings (e.g., 'As a Senior Data Engineer, how would you approach...')."

**Inner Meaning & Outcome:**
This ensured that the project was completely resilient to API rate limits or missing environment variables during the judging process. By dynamically injecting the `jobRole` into hardcoded fallback strings, the app maintains the illusion of an adaptive, role-based AI even when completely disconnected from the internet.
