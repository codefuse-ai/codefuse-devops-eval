import json

from loguru import logger

import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig

from src.model_and_tokenizer_loader.model_and_tokenizer_loader import ModelAndTokenizerLoader

def load_model_and_tokenizer(eval_args):
    '''
    Load model and tokenizer by model_path and model_name
    '''
    with open(eval_args.model_conf_path, 'r') as f:
        model_conf = json.load(f)
    
    loader = globals()[model_conf[eval_args.model_name]['loader']]()

    return loader.load_model_and_tokenizer(eval_args.model_path)

class QwenModelAndTokenizerLoader(ModelAndTokenizerLoader):
    def __init__(self):
        super().__init__()
        pass

    def load_model(self, model_path: str):
        model = super().load_model(model_path)
        model.generation_config = GenerationConfig.from_pretrained(model_path)

        return model

    def load_tokenizer(self, model_path: str):
        tokenizer = super().load_tokenizer(model_path)

        # read generation config
        with open(model_path + '/generation_config.json', 'r') as f:
            generation_config = json.load(f)
        
        tokenizer.pad_token_id = generation_config['pad_token_id']
        tokenizer.eos_token_id = generation_config['eos_token_id']
        return tokenizer

class BaichuanModelAndTokenizerLoader(ModelAndTokenizerLoader):
    def __init__(self):
        super().__init__()
        pass

    def load_model(self, model_path: str):
        model = super().load_model(model_path)
        # model.generation_config = GenerationConfig.from_pretrained(model_path)

        return model


if __name__ == '__main__':
    model_path = '/mnt/llm/devopspal/model/Qwen-7B'
    qwen_model_loader = QwenModelAndTokenizerLoader()
    tokenizer = qwen_model_loader.load_tokenizer(model_path)

    logger.info(tokenizer)
