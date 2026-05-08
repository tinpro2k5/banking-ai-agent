"""Policy retrieval node — delegates all lookup to BankingPolicies."""

from app.data.policies import BankingPolicies
from app.core.schemas import PolicyResult


class PolicyNode:
    """Retrieves the relevant banking policy for a detected intent.

    All casing / normalisation logic lives in :class:`BankingPolicies`;
    this node is a thin adapter that feeds the intent label in and
    returns a :class:`PolicyResult`.
    """

    def __init__(self) -> None:
        self._banking_policies = BankingPolicies()

    def run(self, intent: str) -> PolicyResult:
        policy_text = self._banking_policies.get_policy(intent)
        return PolicyResult(policy_text=policy_text)