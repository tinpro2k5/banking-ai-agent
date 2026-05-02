from app.nodes.intent_node import IntentNode
from app.nodes.priority_node import PriorityNode
from app.nodes.policy_node import PolicyNode
from app.nodes.draft_node import DraftNode
from app.nodes.validation_node import ValidationNode
from app.nodes.router_node import RouterNode
from app.core.schemas import AgentResponse

class Orchestrator:
    def __init__(self):
        self.intent_node = IntentNode()
        self.priority_node = PriorityNode()
        self.policy_node = PolicyNode()
        self.draft_node = DraftNode()
        self.validation_node = ValidationNode()
        self.router_node = RouterNode()

    def run(self, message: str) -> AgentResponse:
        intent_result = self.intent_node.run(message)
        priority_result = self.priority_node.run(message, intent_result.intent)
        policy_result = self.policy_node.run(intent_result.intent)
        draft_result = self.draft_node.run(
            message, intent_result.intent, priority_result.level, policy_result.policy_text
        )
        validation_result = self.validation_node.run(
            draft_result.draft, intent_result.intent, intent_result.confidence
        )
        router_result = self.router_node.run(
            priority_result.level, validation_result.valid, intent_result.confidence
        )

        if router_result.action == "escalate":
            final_reply = "Your case has been escalated to a human agent. We will contact you shortly."
        elif router_result.action == "ask_more":
            final_reply = "Could you please provide more details about your issue so we can assist you better?"
        else:
            final_reply = draft_result.draft

        return AgentResponse(
            intent=intent_result,
            priority=priority_result,
            policy=policy_result,
            draft=draft_result,
            validation=validation_result,
            routing=router_result,
            final_reply=final_reply
        )