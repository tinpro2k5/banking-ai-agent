from app.core.schemas import RouterResult

class RouterNode:
    def run(self, priority: str, valid: bool, confidence: float) -> RouterResult:
        if priority == "high" or not valid:
            return RouterResult(action="escalate", reason="High priority or validation failed — requires human agent.")
        if confidence < 0.6:
            return RouterResult(action="ask_more", reason="Low confidence — need more information from customer.")
        return RouterResult(action="reply", reason="Workflow completed successfully.")