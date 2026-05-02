"""Banking policies and rules."""

# Policy rules
POLICIES = {
    "transfer_not_received_by_recipient": "Transfers may take 1-3 business days. If funds are not received after 3 days, file a trace request with transaction ID.",
    "card_not_received": "Cards are dispatched within 5 business days. Contact support if not received after 10 days.",
    "blocked_card": "Cards are blocked for security. Customer must verify identity via OTP or visit a branch.",
    "refund_not_received": "Refunds take 5-7 business days. If not received, provide merchant receipt for investigation.",
    # ... add ~10-15 more covering common BANKING77 intents
}
DEFAULT_POLICY = "Please contact our support team for assistance with your inquiry."

class BankingPolicies:
    """Banking policies and business rules."""

    def __init__(self):
        """Initialize policies."""
        self.policies = POLICIES
        self.default_policy = DEFAULT_POLICY


    @staticmethod
    def get_policy(policy_type: str) -> dict:
        """Get policy for a given type."""
        return BankingPolicies.POLICIES.get(policy_type, {"text": BankingPolicies.DEFAULT_POLICY})

