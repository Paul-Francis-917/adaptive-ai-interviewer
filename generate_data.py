import os
import json

def main():
    os.makedirs('backend/data', exist_ok=True)
    os.makedirs('backend/app/api', exist_ok=True)
    os.makedirs('backend/app/services', exist_ok=True)
    os.makedirs('backend/app/models', exist_ok=True)
    os.makedirs('backend/app/prompts', exist_ok=True)
    
    curriculum = [
        {"day": 1, "title": "VS Code & Python Environment Setup", "type": "SETUP", "tools": ["VS Code", "Python", "Python Extension", "Pylance"], "objectives": ["Understand basic IDE setup", "Configure Python path"]},
        {"day": 2, "title": "Local LLM & AI Coding Assistant Setup", "type": "SETUP", "tools": ["Ollama", "Qwen2.5-Coder", "GitHub Copilot", "Cline"], "objectives": ["Install and run local models", "Use AI extensions in VS Code"]},
        {"day": 3, "title": "First AI Project, React Frontend & GitHub", "type": "BUILD", "tools": ["Python", "Ollama", "FastAPI", "React"], "objectives": ["Create a basic full-stack app", "Initialize version control"]},
        {"day": 4, "title": "Reading & Processing Structured Data", "type": "BUILD", "tools": ["Pandas", "SQLite", "SQL", "SQLAlchemy"], "objectives": ["Read CSVs", "Write to SQLite database"]},
        {"day": 5, "title": "Reading & Processing Unstructured Data", "type": "BUILD", "tools": ["pdfplumber", "PyPDF", "python-docx", "Tesseract OCR"], "objectives": ["Extract text from PDFs", "Run basic OCR"]},
        {"day": 6, "title": "Building the Knowledge Base", "type": "BUILD", "tools": ["LangChain Text Splitters", "JSONL", "Python"], "objectives": ["Chunk text for retrieval", "Store chunks in JSONL format"]},
        {"day": 7, "title": "Embeddings Explained", "type": "AI_CORE", "tools": ["Sentence Transformers", "OpenAI Embeddings", "Scikit-learn", "Matplotlib"], "objectives": ["Understand vector representations", "Generate embeddings from text"]},
        {"day": 8, "title": "Vector Databases Overview", "type": "BUILD", "tools": ["ChromaDB", "Pinecone"], "objectives": ["Initialize vector database", "Understand indexing"]},
        {"day": 9, "title": "Building & Populating the Vector Database", "type": "BUILD", "tools": ["ChromaDB", "Sentence Transformers"], "objectives": ["Insert text chunks into ChromaDB", "Query inserted vectors"]},
        {"day": 10, "title": "The Retrieval & Matching Engine", "type": "SHIP_IT", "tools": ["SQLite", "ChromaDB", "Python"], "objectives": ["Combine metadata filtering and vector search", "Return top K results"]},
        {"day": 11, "title": "RAG End-to-End & LLM API Basics", "type": "BUILD", "tools": ["OpenAI SDK", "Ollama", "Groq", "Python"], "objectives": ["Pass retrieved chunks to LLM prompt", "Generate response from context"]},
        {"day": 12, "title": "Prompt Engineering Fundamentals", "type": "LEARN", "tools": ["LLMs", "Prompt Templates"], "objectives": ["Write clear instructions", "Use few-shot prompting"]},
        {"day": 13, "title": "Advanced Prompting: Function Calling & Structured Outputs", "type": "BUILD", "tools": ["OpenAI Function Calling", "Pydantic", "Python"], "objectives": ["Define JSON schemas for LLM outputs", "Parse structured output safely"]},
        {"day": 14, "title": "Fine-Tuning: Concepts & When to Use It", "type": "LEARN", "tools": ["JSONL", "OpenAI", "LoRA", "QLoRA"], "objectives": ["Understand fine-tuning use cases", "Format datasets for tuning"]},
        {"day": 15, "title": "Fine-Tuning: Hands-On with LoRA & QLoRA", "type": "SHIP_IT", "tools": ["PEFT", "Transformers", "BitsAndBytes", "OpenAI Fine-Tuning"], "objectives": ["Train a small adapter", "Evaluate tuned model"]},
        {"day": 16, "title": "Chatbot Backend & API Integration", "type": "BUILD", "tools": ["FastAPI", "SQLite", "Python"], "objectives": ["Create chat endpoints", "Store message history"]},
        {"day": 17, "title": "Chatbot Frontend Development", "type": "BUILD", "tools": ["Streamlit", "Requests", "UUID"], "objectives": ["Build a simple chat UI", "Connect to FastAPI backend"]},
        {"day": 18, "title": "Full-Stack Integration & Streaming Responses", "type": "BUILD", "tools": ["FastAPI", "StreamingResponse", "Server-Sent Events", "Streamlit"], "objectives": ["Stream tokens from backend to frontend", "Handle connection drops"]},
        {"day": 19, "title": "Response Formatting & Rich Outputs", "type": "BUILD", "tools": ["Pydantic", "Markdown", "Streamlit"], "objectives": ["Render markdown in UI", "Parse tables and code blocks"]},
        {"day": 20, "title": "Conversation Memory & Context Management", "type": "SHIP_IT", "tools": ["SQLite", "FastAPI", "LLM", "Token Management"], "objectives": ["Summarize long histories", "Implement rolling window memory"]},
        {"day": 21, "title": "Agentic Frameworks: LangChain Agents & Tool Use", "type": "BUILD", "tools": ["LangChain", "LangChain Agents", "ReAct", "Python"], "objectives": ["Create agents with tool access", "Understand ReAct prompt logic"]},
        {"day": 22, "title": "Multi-Agent Orchestration", "type": "BUILD", "tools": ["CrewAI", "LangGraph", "Python"], "objectives": ["Define multiple agents with roles", "Pass state between agents"]},
        {"day": 23, "title": "Model Context Protocol (MCP)", "type": "BUILD", "tools": ["MCP Python SDK", "Claude Desktop", "Cline", "Python"], "objectives": ["Build MCP servers", "Connect tools securely"]},
        {"day": 24, "title": "Agentic Chatbot Integration", "type": "SHIP_IT", "tools": ["LangChain", "MCP", "FastAPI", "Python"], "objectives": ["Combine chat UI with agent logic", "Handle long-running agent tasks"]},
        {"day": 25, "title": "Chatbot Evaluation & Testing", "type": "SHIP_IT", "tools": ["Python", "Evaluation Dataset", "Automated Testing"], "objectives": ["Write deterministic tests for LLMs", "Use LLM-as-a-judge patterns"]},
        {"day": 26, "title": "Performance Optimization & Cost Management", "type": "OPTIMIZE", "tools": ["tiktoken", "Python", "FastAPI"], "objectives": ["Count tokens accurately", "Implement caching strategies"]},
        {"day": 27, "title": "Security, Privacy & Guardrails", "type": "BUILD", "tools": ["FastAPI", "Python", "Authentication", "Input Validation"], "objectives": ["Detect prompt injection", "Sanitize LLM outputs"]},
        {"day": 28, "title": "Docker & Kubernetes Deployment", "type": "SHIP_IT", "tools": ["Docker", "Kubernetes", "FastAPI", "React"], "objectives": ["Write Dockerfiles for frontend and backend", "Deploy to cluster"]},
        {"day": 29, "title": "Monitoring, Logging & Observability", "type": "BUILD", "tools": ["Python Logging", "Prometheus", "Grafana"], "objectives": ["Track API latency", "Log LLM request durations"]},
        {"day": 30, "title": "Production Readiness & Final Testing", "type": "SHIP_IT", "tools": ["FastAPI", "Docker", "Kubernetes", "Python"], "objectives": ["Run load tests", "Configure health checks"]},
        {"day": 31, "title": "Capstone Project & Final Demo", "type": "CAPSTONE", "tools": ["FastAPI", "React", "LangChain", "MCP"], "objectives": ["Complete end-to-end project", "Prepare demo presentation"]}
    ]
    
    with open('backend/data/curriculum.json', 'w') as f:
        json.dump(curriculum, f, indent=2)

    candidates = [
        {
            "member": {
                "id": "CAND-001",
                "name": "Sarah Johnson",
                "jobRole": "Senior Data Engineer",
                "yearsExperience": 5,
                "education": "BSc Computer Science",
                "status": "active"
            },
            "missions": [
                {"day": 7, "title": "Embeddings Explained", "passed": True, "attempts": 1},
                {"day": 10, "title": "The Retrieval & Matching Engine", "passed": True, "attempts": 2},
                {"day": 12, "title": "Prompt Engineering Fundamentals", "passed": True, "attempts": 4},
                {"day": 22, "title": "Multi-Agent Orchestration", "passed": True, "attempts": 1},
                {"day": 23, "title": "Model Context Protocol (MCP)", "passed": True, "attempts": 1},
                {"day": 28, "title": "Docker & Kubernetes Deployment", "passed": True, "attempts": 3},
                {"day": 29, "title": "Monitoring, Logging & Observability", "skipped": True}
            ],
            "signals": {
                "commitDays": 20,
                "missionsCompleted": 25,
                "missionsFirstTry": 15
            }
        },
        {
            "member": {
                "id": "CAND-002",
                "name": "Alex Chen",
                "jobRole": "Junior Full Stack Developer",
                "yearsExperience": 1,
                "education": "Bootcamp Graduate",
                "status": "active"
            },
            "missions": [
                {"day": 3, "title": "First AI Project, React Frontend & GitHub", "passed": True, "attempts": 1},
                {"day": 16, "title": "Chatbot Backend & API Integration", "passed": True, "attempts": 2},
                {"day": 17, "title": "Chatbot Frontend Development", "passed": True, "attempts": 1},
                {"day": 18, "title": "Full-Stack Integration & Streaming Responses", "passed": True, "attempts": 3},
                {"day": 19, "title": "Response Formatting & Rich Outputs", "passed": True, "attempts": 2},
                {"day": 20, "title": "Conversation Memory & Context Management", "passed": False, "attempts": 5}
            ],
            "signals": {
                "commitDays": 15,
                "missionsCompleted": 18,
                "missionsFirstTry": 10
            }
        }
    ]
    
    with open('backend/data/candidates.json', 'w') as f:
        json.dump(candidates, f, indent=2)

    with open('technical-spec.md', 'w') as f:
        f.write("# Technical Specification\n\nExact HTTP API contract. The API expects a POST to `/api/interview`.\n\n## 1. Start Interview\n**POST `/api/interview`**\n```json\n{\n  \"sessionId\": \"abc-123\",\n  \"candidate\": { ...candidate object... }\n}\n```\nResponse:\n```json\n{\n  \"reply\": \"Welcome. Let's begin your interview.\",\n  \"done\": false\n}\n```\n\n## 2. Continue Interview\n**POST `/api/interview`**\n```json\n{\n  \"sessionId\": \"abc-123\",\n  \"message\": \"My answer to the previous question...\"\n}\n```\nResponse:\n```json\n{\n  \"reply\": \"...next interviewer reply...\",\n  \"done\": false\n}\n```\n\n## 3. End Interview\nResponse:\n```json\n{\n  \"reply\": \"Interview completed.\",\n  \"done\": true,\n  \"feedback\": {\n    \"summary\": \"...\",\n    \"strengths\": [\"...\"],\n    \"gaps\": [\"...\"],\n    \"next\": [\"...\"]\n  }\n}\n```\n")

if __name__ == '__main__':
    main()
