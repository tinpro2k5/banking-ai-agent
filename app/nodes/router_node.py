from typing import Optional

from app.core.schemas import RouterResult

class RouterNode:
    def run(
        self,
        priority: str,
        valid: bool,
        intent: str,
        confidence: Optional[float],
        missing_info: Optional[str] = None,
    ) -> RouterResult:
        if priority == "high" or not valid:
            return RouterResult(action="escalate", reason="High priority or validation failed — requires human agent.")
        if missing_info:
            return RouterResult(action="ask_more", reason="Draft requires additional information from the customer.")
        if intent == "unknown_intent":
            return RouterResult(action="ask_more", reason="Intent could not be identified confidently.")
        if confidence is not None and confidence < 0.6:
            return RouterResult(action="ask_more", reason="Low confidence — need more information from customer.")
        return RouterResult(action="reply", reason="Workflow completed successfully.")