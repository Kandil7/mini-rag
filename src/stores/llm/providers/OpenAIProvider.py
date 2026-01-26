from ..LLMInterface import LLMInterface
from ..LLMEnum import OpenAIEnums
from openai import (
    OpenAI,
    RateLimitError,
    APIError,
    APIConnectionError,
    BadRequestError,
    AuthenticationError,
    PermissionDeniedError,
    NotFoundError,
)
import httpx
import logging

class OpenAIProvider(LLMInterface):

    def __init__(self, api_key: str, api_url: str=None,
                       default_input_max_characters: int=1000,
                       default_generation_max_output_tokens: int=1000,
                       default_generation_temperature: float=0.1):
        
        self.api_key = api_key
        self.api_url = api_url

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        if self.api_key:
            # Use an explicit httpx client to avoid proxy args incompatibilities on older httpx versions.
            http_client = httpx.Client()
            self.client = OpenAI(
                api_key = self.api_key,
                base_url = self.api_url if self.api_url else None,
                http_client = http_client,
            )
        else:
            self.client = None

        self.last_error_type = None
        self.logger = logging.getLogger(__name__)

    def _clear_error(self):
        self.last_error_type = None

    def _set_error(self, error_type: str, message: str):
        self.last_error_type = error_type
        self.logger.error(message)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None,
                            temperature: float = None):

        self._clear_error()

        if not self.client:
            self.logger.error("OpenAI client was not set")
            return None

        if not self.generation_model_id:
            self.logger.error("Generation model for OpenAI was not set")
            return None

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        chat_history_copy = chat_history.copy()  # Avoid modifying the original list
        chat_history_copy.append(
            self.construct_prompt(prompt=prompt, role=OpenAIEnums.USER.value)
        )

        try:
            response = self.client.chat.completions.create(
                model = self.generation_model_id,
                messages = chat_history_copy,
                max_tokens = max_output_tokens,
                temperature = temperature
            )
        except RateLimitError as exc:
            self._set_error("rate_limit", f"OpenAI rate limit exceeded: {exc}")
            return None
        except (AuthenticationError, PermissionDeniedError) as exc:
            self._set_error("auth", f"OpenAI auth error: {exc}")
            return None
        except (BadRequestError, NotFoundError) as exc:
            self._set_error("request", f"OpenAI request error: {exc}")
            return None
        except (APIConnectionError, APIError) as exc:
            self._set_error("api", f"OpenAI API error: {exc}")
            return None
        except Exception as exc:
            self._set_error("unknown", f"Unexpected OpenAI error: {exc}")
            return None

        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message:
            self.logger.error("Error while generating text with OpenAI")
            return None

        return response.choices[0].message.content


    def embed_text(self, text: str, document_type: str = None):

        self._clear_error()

        if not self.client:
            self.logger.error("OpenAI client was not set")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model for OpenAI was not set")
            return None

        try:
            response = self.client.embeddings.create(
                model = self.embedding_model_id,
                input = text,
            )
        except RateLimitError as exc:
            self._set_error("rate_limit", f"OpenAI rate limit exceeded: {exc}")
            return None
        except (AuthenticationError, PermissionDeniedError) as exc:
            self._set_error("auth", f"OpenAI auth error: {exc}")
            return None
        except (BadRequestError, NotFoundError) as exc:
            self._set_error("request", f"OpenAI request error: {exc}")
            return None
        except (APIConnectionError, APIError) as exc:
            self._set_error("api", f"OpenAI API error: {exc}")
            return None
        except Exception as exc:
            self._set_error("unknown", f"Unexpected OpenAI error: {exc}")
            return None

        if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("Error while embedding text with OpenAI")
            return None

        return response.data[0].embedding

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "content": self.process_text(prompt)
        }
    


    
