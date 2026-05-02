from app.clients.ollama_client import OllamaClient
from app.core.schemas import DraftResult

class DraftNode:
    def __init__(self):
        self.client = OllamaClient()

    def run(self, message: str, intent: str, priority: str, policy: str) -> DraftResult:
        prompt = f"""You are a banking customer support agent.

Customer message: {message}
Detected intent: {intent}
Priority level: {priority}
Relevant policy: {policy}

Write a polite, concise reply to the customer. If information is missing, note it.
Reply:"""
        draft = self.client.generate(prompt)
        return DraftResult(draft=draft.strip(), missing_info=None)