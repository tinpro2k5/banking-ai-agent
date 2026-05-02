from app.core.schemas import ValidationResult

class ValidationNode:
    def run(self, draft: str, intent: str, confidence: float) -> ValidationResult:
        issues = []
        if len(draft) < 30:
            issues.append("Draft is too short.")
        if confidence < 0.5:
            issues.append(f"Low intent confidence: {confidence}")
        if not any(word in draft.lower() for word in ["account", "card", "transfer", "refund", "team", "support", "transaction"]):
            issues.append("Draft may lack banking-specific content.")
        valid = len(issues) == 0
        return ValidationResult(valid=valid, issues="; ".join(issues) if issues else None)