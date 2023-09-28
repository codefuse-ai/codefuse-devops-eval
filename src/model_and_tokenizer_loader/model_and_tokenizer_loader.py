import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig


class ModelAndTokenizerLoader:
    def __init__(self):
        pass

    def load_model_and_tokenizer(self, model_path: str):
        model = self.load_model(model_path)
        tokenizer = self.load_tokenizer(model_path)
        return model, tokenizer

    def load_model(self, model_path: str):
        model =  AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", trust_remote_code=True).eval()
        return model

    def load_tokenizer(self, model_path: str):
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        return tokenizer

