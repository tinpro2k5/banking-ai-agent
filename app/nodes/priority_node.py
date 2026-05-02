from app.core.schemas import PriorityResult

HIGH_PRIORITY_KEYWORDS = ["fraud", "stolen", "unauthorized", "blocked", "lost", "scam", "hack"]
MEDIUM_PRIORITY_KEYWORDS = ["not received", "failed", "error", "wrong amount", "refund"]

class PriorityNode:
    def run(self, message: str, intent: str) -> PriorityResult:
        msg = message.lower()
        if any(k in msg for k in HIGH_PRIORITY_KEYWORDS):
            return PriorityResult(level="high", reason="Message contains urgent/security keywords.")
        if any(k in msg for k in MEDIUM_PRIORITY_KEYWORDS):
            return PriorityResult(level="medium", reason="Message indicates a transaction issue.")
        return PriorityResult(level="low", reason="Routine inquiry.")