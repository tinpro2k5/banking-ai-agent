from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from app.core.settings import INTENT_MODEL_PATH
from app.core.schemas import IntentResult

class IntentNode:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(INTENT_MODEL_PATH)
        self.model = AutoModelForSequenceClassification.from_pretrained(INTENT_MODEL_PATH)
        self.model.eval()

    def run(self, message: str) -> IntentResult:
        inputs = self.tokenizer(message, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = self.model(**inputs).logits
        probs = torch.softmax(logits, dim=-1)
        confidence, pred = probs.max(dim=-1)
        intent_label = self.model.config.id2label[pred.item()]
        return IntentResult(intent=intent_label, confidence=round(confidence.item(), 3))