"""Intent detection node — calls the remote intent inference server on Colab."""
import requests
from app.core.settings import settings
from app.core.schemas import IntentResult


class IntentNode:
    """Calls the remote intent classifier server exposed via Pinggy."""

    def run(self, message: str) -> IntentResult:
        try:
            response = requests.post(
                settings.intent_api_url,
                json={"message": message},
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as exc:
            # Intent server unreachable or returned an error — degrade safely.
            # Log the problem (print here to keep dependencies minimal) and return unknown_intent.
            print(f"[Warning] intent server error: {exc}")
            return IntentResult(intent="unknown_intent", confidence=None)

        confidence = data.get("confidence")
        if confidence is not None:
            try:
                confidence = float(confidence)
            except (TypeError, ValueError):
                confidence = None
        return IntentResult(
            intent=data.get("intent", "unknown_intent"),
            confidence=confidence,
        )
