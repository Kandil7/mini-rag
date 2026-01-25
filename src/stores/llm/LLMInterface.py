from abc import ABC ,abstractmethod
class LLMInterface(ABC):
    @abstractmethod
    def set_generation_model(self,model_id:str):
        pass
    
    @abstractmethod
    def set_embbeding_model(slef,model_id:str,embbeding_size:int):
        pass

    @abstractmethod
    def generate_text(
        self,
        prompt:str,
        chat_history:list=[],
        temperature:float=None
        ):
        pass
    @abstractmethod
    def embed_text(self,text:str,document_type:str=None):
        pass
    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        pass