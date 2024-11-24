from langchain.llms.base import BaseLLM
from typing import Optional, List
from langchain.schema import LLMResult, Generation
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

    def _generate(self, prompts: List[str], stop: Optional[List[str]] = None) -> LLMResult:
        """
        Generate responses from the Together AI LLM for a list of prompts.
        """
        if stop is None:
            stop = ["<|eot_id|>", "<|eom_id|>"]

        generations = []

        for prompt in prompts:
            # Request a response from the Together API
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

            # Parse the response and add to the generations list
            if response and hasattr(response, "choices") and response.choices:
                content = response.choices[0].message.content.strip()
                generations.append(Generation(text=content))
            else:
                generations.append(Generation(text="No response from Together API."))

        return LLMResult(generations=[generations])
