from langchain.llms.base import BaseLLM
from typing import Optional, List
from together import Together

class TogetherLLM(BaseLLM):
    def __init__(self, model: str, max_tokens: int = 512, temperature: float = 0.7, top_p: float = 0.7, top_k: int = 50):
        """
        Initialize the TogetherLLM wrapper.
        """
        self.client = Together()
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k

    @property
    def _llm_type(self) -> str:
        return "TogetherAI"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """
        Generate a response from Together AI LLaMA model.
        """
        if stop is None:
            stop = ["<|eot_id|>", "<|eom_id|>"]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            top_k=self.top_k,
            stop=stop,
            stream=False,
        )

        # Parse response
        if response and hasattr(response, "choices"):
            return response.choices[0].message["content"].strip()
        else:
            return "No response from Together API."
