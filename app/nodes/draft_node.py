import re
from app.clients.ollama_client import OllamaClient
from app.core.schemas import DraftResult

# Matches bracketed placeholders the LLM emits when it needs missing details,
# e.g. [transaction ID], [account number], [date of transfer].
# Length bounds (3–50 chars) avoid false positives on abbreviations like [1]
# or runaway matches on malformed output.
_PLACEHOLDER_RE = re.compile(r"\[([^\]]{3,50})\]")


class DraftNode:
    def __init__(self):
        self.client = OllamaClient()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_missing_info(draft: str) -> str | None:
        """Return a comma-separated list of placeholder tokens found in *draft*,
        or ``None`` if the draft looks complete."""
        matches = _PLACEHOLDER_RE.findall(draft)
        if not matches:
            return None
        # De-duplicate while preserving order.
        seen: set[str] = set()
        unique = [m for m in matches if not (m in seen or seen.add(m))]  # type: ignore[func-returns-value]
        return "Missing: " + ", ".join(unique)

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def run(self, message: str, intent: str, priority: str, policy: str) -> DraftResult:
        prompt = f"""You are a banking customer support agent.

Customer message: {message}
Detected intent: {intent}
Priority level: {priority}
Relevant policy: {policy}

Write a polite, concise reply to the customer. If you need more information \
(such as a transaction ID, date, or account number) to resolve the issue, \
write the required field name inside square brackets, e.g. [transaction ID].
Reply:"""
        draft = self.client.generate(prompt).strip()
        missing_info = self._extract_missing_info(draft)
        return DraftResult(draft=draft, missing_info=missing_info)