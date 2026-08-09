# adaptive-ai-interviewer Requirements

Based on the technical-spec.md, curriculum.json, and candidates.json, here are the core requirements and constraints for the hackathon project:

## 1. Exact API Contract
The backend MUST expose a single endpoint: `POST /api/interview`

### A. Start Interview (Request)
```json
{
  "sessionId": "abc-123",
  "candidate": {
    "id": "CAND-...",
    ...
  }
}
```

### B. Continue Interview (Request)
```json
{
  "sessionId": "abc-123",
  "message": "Candidate's answer text..."
}
```

### C. Standard Response
```json
{
  "reply": "Interviewer's next question or statement...",
  "done": false
}
```

### D. Final Response (End Interview)
```json
{
  "reply": "Final closing statement.",
  "done": true,
  "feedback": {
    "summary": "2-4 sentences describing overall interview performance",
    "strengths": ["Specific demonstrated strength 1", "..."],
    "gaps": ["Specific missing concept 1", "..."],
    "next": ["Concrete next step 1", "..."]
  }
}
```

## 2. Hard Constraints (Minimums)
- **Minimum 8 questions:** The interview must never return `done: true` before 8 questions are asked.
- **Minimum 4 unique curriculum days:** The interview must touch upon at least 4 different days from the curriculum.json.
- **Adaptive:** Follow-up questions must use previous answers.
- **Stateful:** The `sessionId` must be used to reload the interview state on every request. No authentication is required.

## 3. Core Data
- `curriculum.json`: 31 days of AI engineering curriculum (our knowledge base for grounding).
- `candidates.json`: Synthetic learner profiles containing missions (passed/skipped) and attempt signals. We must use this to plan the interview topics.
