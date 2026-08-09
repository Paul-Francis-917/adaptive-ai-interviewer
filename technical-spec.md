# Technical Specification

Exact HTTP API contract. The API expects a POST to `/api/interview`.

## 1. Start Interview
**POST `/api/interview`**
```json
{
  "sessionId": "abc-123",
  "candidate": { ...candidate object... }
}
```
Response:
```json
{
  "reply": "Welcome. Let's begin your interview.",
  "done": false
}
```

## 2. Continue Interview
**POST `/api/interview`**
```json
{
  "sessionId": "abc-123",
  "message": "My answer to the previous question..."
}
```
Response:
```json
{
  "reply": "...next interviewer reply...",
  "done": false
}
```

## 3. End Interview
Response:
```json
{
  "reply": "Interview completed.",
  "done": true,
  "feedback": {
    "summary": "...",
    "strengths": ["..."],
    "gaps": ["..."],
    "next": ["..."]
  }
}
```
