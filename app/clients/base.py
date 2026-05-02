from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    """Abstract base client."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass
