from pydantic import BaseModel


class GenerateConfigs(BaseModel):
    max_new_tokens: int = 128
    beam_bums: int = 1
    top_k: int = 50
    top_p: float = 0.95
    temperature: float = 1.0
    length_penalty: float = 1.0
    presence_penalty: float = 1.0
    stop_words: list = []
    template: str = "default"