# AI Usage Log

This document records the usage of AI coding assistants during the hackathon to fulfill the submission requirements.

## Overview
The project was built with the assistance of Google's **Gemini 3.1 Pro** via the Antigravity IDE framework. We used the "Vibe Coding" phase-by-phase approach outlined in the official hackathon blueprint.

## Key Prompts & Tasks

1. **Phase 1: Planning and Setup**
   - **Task:** "Read curriculum.json, candidates.json and technical-spec.md and scaffold the project."
   - **Result:** The AI created `docs/requirements.md` mapping out the API contracts and validated the frontend/backend scaffolding.

2. **Phase 2: Core Data Services**
   - **Task:** "Parse curriculum JSON and build day lookup. Parse candidate object."
   - **Result:** The AI built `curriculum_service.py` to index the 31 days into memory and `profile_service.py` to classify candidate missions into passed/skipped arrays.

3. **Phase 3: Interview State and Logic**
   - **Task:** "Select 5 diverse completed days and mark 4 as mandatory anchors. Implement start vs continue logic."
   - **Result:** The AI created `planner.py` to ensure diverse topic selection and `session_store.py` to track the state in an in-memory dictionary.

4. **Phase 4: AI Engine**
   - **Task:** "Implement adaptive LLM engine and coverage guard."
   - **Result:** The AI wrote `llm_service.py` integrating the `google-generativeai` SDK to evaluate answers and generate feedback in JSON format. It also wrote the critical coverage guard in `interview_engine.py` preventing early finishes before 8 questions / 4 days.

5. **Phase 5: Integration and UI**
   - **Task:** "Implement the POST /api/interview endpoint exactly. Redesign the frontend for the ABTalks 60 Day Challenge."
   - **Result:** The AI wired the FastAPI endpoint and completely redesigned `App.tsx` into a responsive, mobile-first experience using TailwindCSS.

6. **Phase 6: QA and Testing**
   - **Task:** "Add end-to-end API tests."
   - **Result:** The AI wrote `pytest` tests using `TestClient` to ensure the session continuity and guardrails work.

## Modifications Made Manually
- Relaxed strict versions in `requirements.txt` to support modern Python environments without C++ build tool dependencies.
- Bootstrapped initial Git repository and linked to remote GitHub.
