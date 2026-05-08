"""FastAPI application — registers routes and creates the server object."""

from fastapi import FastAPI
from app.core.schemas import CustomerRequest, AgentResponse
from app.agent.orchestrator import Orchestrator

app = FastAPI(title="Banking AI Agent")
orchestrator = Orchestrator()


@app.post("/chat", response_model=AgentResponse)
def chat(request: CustomerRequest):
    return orchestrator.run(request.message)


@app.get("/health")
def health():
    return {"status": "ok"}
