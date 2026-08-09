from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api import interview

app = FastAPI(title="AI Interview Agent")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interview.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}
