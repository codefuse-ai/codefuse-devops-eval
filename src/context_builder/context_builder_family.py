import json

from loguru import logger
from src.context_builder.context_builder import ContextBuilder

def get_context_builder(eval_args):
    '''
    Load context_builder by model_name
    '''
    with open(eval_args.model_conf_path, 'r') as f:
        model_conf = json.load(f)
    
    context_builder = globals()[model_conf[eval_args.model_name]['context_builder']]()
    return context_builder

class QwenChatContextBuilder(ContextBuilder):
    def __init__(self):
        super().__init__()
    
    def make_context(
        self,
        model,
        tokenizer, 
        query: str,
        system: str = "you are a helpful assistant"
    ):
        im_start, im_end = "<|im_start|>", "<|im_end|>"
        im_start_tokens = [tokenizer.im_start_id]
        im_end_tokens = [tokenizer.im_end_id]
        nl_tokens = tokenizer.encode("\n")

        def _tokenize_str(role, content):
            return f"{role}\n{content}", tokenizer.encode(
                role, allowed_special=set()
            ) + nl_tokens + tokenizer.encode(content, allowed_special=set())

        system_text, system_tokens_part = _tokenize_str("system", system)
        system_tokens = im_start_tokens + system_tokens_part + im_end_tokens

        raw_text = ""
        context_tokens = []

        context_tokens = system_tokens + context_tokens
        raw_text = f"{im_start}{system_text}{im_end}" + raw_text
        context_tokens += (
            nl_tokens
            + im_start_tokens
            + _tokenize_str("user", query)[1]
            + im_end_tokens
            + nl_tokens
            + im_start_tokens
            + tokenizer.encode("assistant")
            + nl_tokens
        )
        raw_text += f"\n{im_start}user\n{query}{im_end}\n{im_start}assistant\n"
        return raw_text, context_tokens

class Baichuan2ChatContextBuilder(ContextBuilder):
    def __init__(self):
        super().__init__()
    
    def make_context(
        self,
        model,
        tokenizer, 
        query: str,
        system: str = "you are a helpful assistant"
    ):
        messages = []
        messages.append({"role": "user", "content": query})

        raw_text, context_tokens = self.build_chat_input(model, tokenizer, messages)

        return raw_text, context_tokens
    
    def build_chat_input(self, model, tokenizer, messages, max_new_tokens: int=0):
        def _parse_messages(messages, split_role="user"):
            system, rounds = "", []
            round = []
            for i, message in enumerate(messages):
                if message["role"] == "system":
                    assert i == 0
                    system = message["content"]
                    continue
                if message["role"] == split_role and round:
                    rounds.append(round)
                    round = []
                round.append(message)
            if round:
                rounds.append(round)
            return system, rounds

        max_new_tokens = max_new_tokens or model.generation_config.max_new_tokens
        max_input_tokens = model.config.model_max_length - max_new_tokens
        system, rounds = _parse_messages(messages, split_role="user")
        system_tokens = tokenizer.encode(system)
        max_history_tokens = max_input_tokens - len(system_tokens)

        history_tokens = []
        for round in rounds[::-1]:
            round_tokens = []
            for message in round:
                if message["role"] == "user":
                    round_tokens.append(model.generation_config.user_token_id)
                else:
                    round_tokens.append(model.generation_config.assistant_token_id)
                round_tokens.extend(tokenizer.encode(message["content"]))
            if len(history_tokens) == 0 or len(history_tokens) + len(round_tokens) <= max_history_tokens:
                history_tokens = round_tokens + history_tokens  # concat left
                if len(history_tokens) < max_history_tokens:
                    continue
            break

        input_tokens = system_tokens + history_tokens
        if messages[-1]["role"] != "assistant":
            input_tokens.append(model.generation_config.assistant_token_id)
        input_tokens = input_tokens[-max_input_tokens:]  # truncate left

        raw_text = tokenizer.decode(input_tokens)
        return raw_text, input_tokens

class InternlmChatContextBuilder(ContextBuilder):
    def __init__(self):
        super().__init__()
    
    def make_context(
        self,
        model,
        tokenizer, 
        query: str,
        system: str = "you are a helpful assistant"
    ):
        prompt = ""
        if len(prompt) == 0:
            prompt += "<s>"
        prompt += f"""<|User|>:{query}<eoh>\n<|Bot|>:"""
        return prompt, tokenizer.encode(prompt)


if __name__ == '__main__':
    query = '你好'
    system = '请帮助我'
    tokenizer = '/mnt/llm/devopspal/model/Qwen-7B'

