import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from firewall import inspect_prompt

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is missing from .env file!")

app = FastAPI(
    title="LLM Guardrail & Red Teaming API",
    description="A secure LLM backend with firewall protection.",
    version="1.0.0"
)

# Active LLM from your account models list
llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0.7,
    groq_api_key=groq_api_key
)

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # 1. INPUT FIREWALL CHECK
    firewall_result = inspect_prompt(request.prompt)
    
    if not firewall_result["is_safe"]:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "blocked",
                "error": "Security Firewall Violation",
                "reason": firewall_result["reason"],
                "risk_score": firewall_result["risk_score"]
            }
        )

    # 2. LLM EXECUTION (Only reached if prompt passes firewall)
    try:
        response = llm.invoke(request.prompt)
        return {
            "status": "success",
            "prompt": request.prompt,
            "response": response.content,
            "firewall_status": "passed"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "LLM Firewall API is running!"}