"""Intent detection node — calls the remote intent inference server on Colab."""
import requests
from app.core.settings import settings
from app.core.schemas import IntentResult


class IntentNode:
    """Calls the remote intent classifier server exposed via Pinggy."""

    def run(self, message: str) -> IntentResult:
        response = requests.post(
            settings.intent_api_url,
            json={"message": message},
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        confidence = data.get("confidence")
        if confidence is not None:
            try:
                confidence = float(confidence)
            except (TypeError, ValueError):
                confidence = None
        return IntentResult(
            intent=data["intent"],
            confidence=confidence,
        )
