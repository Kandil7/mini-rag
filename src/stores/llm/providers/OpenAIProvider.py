from ..LLMInterface import LLMInterface
from ..LLMEnums import OpenAIEnums
from openai import OpenAI
import logging

class OpenAIProvider(LLMInterface):
    
    def __init__(self,
                 api_key:str,
                 api_url:str=None,
                 default_input_max_charachter:int=1000,
                 default_generation_max_output_tokens:int=1000,
                 default_temperature:float=None

                 ):
        self.api_key=api_key
        self.api_url=api_url
        self.generation_model_id=None
        self.embbeding_model_id=None
        self.embbeding_size=None
        self.client=OpenAI(
            api_key=self.api_key,
            api_url=self.api_url
        )
        self.logger = logging.getLogger(__name__)
    def set_generation_model(self, model_id:str):
        model_id=self.generation_model_id
    
    def set_embbeding_model(self, model_id:str, embbeding_size:int):
        model_id=self.embbeding_model_id
        embbeding_size=self.embbeding_size
    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()
    def generate_text(
    self,
    prompt: str,
    chat_history: list = [],
    max_output_tokens: int = None,
    temperature: float = None,
    ):
        if not self.client:
            self.logger.error("OpenAI client was not set")
            return None

        if not self.generation_model_id:
            self.logger.error("Generation model for OpenAI was not set")
            return None

    
        