"""Banking policies and rules."""

# Policy rules
POLICIES = {
    "transfer_not_received_by_recipient": "Transfers may take 1-3 business days to arrive. If the recipient still has not received the funds after that window, open a trace request with the transaction ID and transfer date.",
    "card_not_received": "Cards are normally dispatched within 5 business days. If the card has not arrived after 10 days, contact support and confirm the mailing address on file.",
    "blocked_card": "Cards are blocked for security reasons until identity is verified. Ask the customer to complete OTP verification or visit a branch for manual support.",
    "refund_not_showing_up": "Refunds typically take 5-7 business days to appear. If the refund is still missing, request the merchant receipt and investigate the payment reference.",
    "activate_my_card": "If the card has arrived, it can usually be activated in the app or through customer support using the last 4 digits and a standard identity check.",
    "card_arrival": "Card delivery usually takes 5-10 business days depending on the region. Ask for the mailing address and any tracking details so the shipment can be verified.",
    "card_payment_fee_charged": "Card payment fees depend on the merchant, card type, and account plan. Review the statement and merchant receipt to confirm whether the charge is expected.",
    "card_payment_not_recognised": "If the customer does not recognize a card payment, first review recent purchases and then dispute the charge with the full transaction details and timestamp.",
    "cash_withdrawal_charge": "ATM withdrawals may include a fee depending on the network and account type. Check the statement for the exact charge description and compare it with the fee schedule.",
    "pending_card_payment": "Pending card payments usually clear within a few business days. If the merchant already confirmed settlement, the customer should contact support with the transaction ID.",
    "pending_transfer": "Pending transfers can take 1-3 business days to complete. Confirm the recipient details, transfer status, and whether the payment has already been settled.",
    "declined_transfer": "Declined transfers are often caused by insufficient funds, beneficiary restrictions, or security checks. Verify the transfer details carefully and ask the customer to try again.",
    "declined_card_payment": "Declined card payments may result from limits, expired cards, or security blocks. Confirm the card status, available balance, and whether the merchant supports the card network.",
    "balance_not_updated_after_bank_transfer": "Transfers may not appear immediately after submission. Wait for settlement, refresh the account history, and only raise a trace if the balance still has not updated.",
    "cash_withdrawal_not_recognised": "If the customer does not recognize an ATM withdrawal, review recent cash activity and request an investigation with the terminal ID, timestamp, and withdrawal amount.",
    "card_linking": "Card linking issues are usually resolved by re-entering the card details, checking the billing address, and confirming the card is enabled for online and recurring use.",
}
DEFAULT_POLICY = "Please contact our support team for assistance with your inquiry."

import re as _re


class BankingPolicies:
    """Banking policies and business rules.

    Encapsulates all policy data and lookup logic.  Nodes should call
    ``get_policy(intent)`` instead of importing ``POLICIES`` directly so that
    casing/normalisation differences between the Lab-2 classifier output and
    the policy keys are handled in one place.
    """

    def __init__(self) -> None:
        self.policies: dict[str, str] = POLICIES
        self.default_policy: str = DEFAULT_POLICY
        # Build a lowercase → original-key map once for fast case-insensitive lookup.
        self._lower_key_map: dict[str, str] = {k.lower(): k for k in POLICIES}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_policy(self, policy_type: str) -> str:
        """Return the policy text for *policy_type*.

        Lookup order (stops at first match):
        1. Exact key match
        2. Case-insensitive key match
        3. Spaces / dashes normalised to underscores
        4. Punctuation stripped (catches labels like ``Refund_not_showing_up``)
        5. Default fallback
        """
        if not policy_type:
            return self.default_policy

        # 1. exact
        if policy_type in self.policies:
            return self.policies[policy_type]

        intent_l = policy_type.lower()

        # 2. lowercase
        orig = self._lower_key_map.get(intent_l)
        if orig:
            return self.policies[orig]

        # 3. spaces / dashes → underscores
        norm = intent_l.replace(" ", "_").replace("-", "_")
        orig = self._lower_key_map.get(norm)
        if orig:
            return self.policies[orig]

        # 4. strip non-alphanumeric/underscore chars
        cleaned = _re.sub(r"[^a-z0-9_]", "", norm)
        orig = self._lower_key_map.get(cleaned)
        if orig:
            return self.policies[orig]

        return self.default_policy

