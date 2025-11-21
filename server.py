# server.py - minimal FastAPI server exposing the orchestrator
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.orchestrator import Orchestrator

app = FastAPI(title='Smart Career Advisor API')
orch = Orchestrator()

class RequestIn(BaseModel):
    user_id: str
    text: str

@app.post('/recommend')
def recommend(req: RequestIn):
    try:
        out = orch.handle(req.user_id, req.text)
        return out
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
