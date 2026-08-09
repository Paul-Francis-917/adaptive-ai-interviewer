# Adaptive AI Interviewer

An intelligent, stateful technical interview evaluation engine built for the **ABTalks 60 Day Challenge**. 

This project does not simply ask a list of questions. Instead, it reads a learner's actual progress from the synthetic cohort dataset, builds a customized interview plan, and dynamically adjusts follow-up questions based on their answers—exactly like a real human interviewer.

## Features
- **Adaptive Questioning:** Generates follow-up questions dynamically based on the exact depth of the candidate's previous response using Google Gemini.
- **Strict Coverage Guard:** Automatically intercepts the LLM to ensure no interview finishes before 8 questions have been asked and 4 distinct curriculum days have been covered.
- **Evidence-based Feedback:** At the end of the interview, generates a structured JSON payload containing a summary, demonstrated strengths, missing gaps, and actionable next steps.
- **Mobile-first UI:** A beautiful, responsive interface designed with Tailwind CSS that allows you to easily simulate an interview from your phone or desktop.

## Folder Structure
- `backend/`: FastAPI Python server containing the core data services, LLM engine, planner, and session store.
- `frontend/`: React + Vite single page application containing the start, chat, and feedback interfaces.
- `docs/`: Original requirements mappings.

## Running Locally

### 1. Start the Backend
You will need a `GEMINI_API_KEY` set in your environment variables.
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2. Start the Frontend
In a new terminal:
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

## Testing
We have included `pytest` automated tests that verify the exact API shape and state continuity.
```bash
cd backend
pytest tests/test_api.py
```
