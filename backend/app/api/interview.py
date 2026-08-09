from fastapi import APIRouter

router = APIRouter()

@router.post("/interview")
async def handle_interview(request: dict):
    return {"reply": "Scaffold works.", "done": False}
