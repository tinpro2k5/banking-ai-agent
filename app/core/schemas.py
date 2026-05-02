from pydantic import BaseModel
from typing import Optional

class CustomerRequest(BaseModel):
    message: str

class IntentResult(BaseModel):
    intent: str
    confidence: float

class PriorityResult(BaseModel):
    level: str  # "low" | "medium" | "high"
    reason: str

class PolicyResult(BaseModel):
    policy_text: str

class DraftResult(BaseModel):
    draft: str
    missing_info: Optional[str]

class ValidationResult(BaseModel):
    valid: bool
    issues: Optional[str]

class RouterResult(BaseModel):
    action: str  # "reply" | "ask_more" | "escalate"
    reason: str

class AgentResponse(BaseModel):
    intent: IntentResult
    priority: PriorityResult
    policy: PolicyResult
    draft: DraftResult
    validation: ValidationResult
    routing: RouterResult
    final_reply: str