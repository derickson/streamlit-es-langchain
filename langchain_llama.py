from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any

from text_generation import Client
from resources import getLlama2Client


class Llama2LLM(LLM):
    
    client : Client = None
    
    def __init__(self):
        super().__init__()  # If LLM has its own constructor, call it with appropriate arguments
        self.client = getLlama2Client()
        
    @property
    def _llm_type(self) -> str:
        return "Llama2"
    


    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        
        text = self.client.generate(
            prompt, 
            temperature=0.01,
            do_sample=True,
            top_k=30,
            max_new_tokens=512,).generated_text
        return text

