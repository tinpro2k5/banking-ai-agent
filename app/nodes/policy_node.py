from app.data.policies import POLICIES, DEFAULT_POLICY
from app.core.schemas import PolicyResult

class PolicyNode:
    def run(self, intent: str) -> PolicyResult:
        text = POLICIES.get(intent, DEFAULT_POLICY)
        return PolicyResult(policy_text=text)