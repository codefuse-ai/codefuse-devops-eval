from loguru import logger
from transformers import PreTrainedTokenizer


class ContextBuilder:
    '''
    Parent class
    '''
    def __init__(self):
        pass

    def make_context(
        self, 
        model,
        tokenizer, 
        query: str,
        system: str = ""
    ):
        '''
        Make context for query, default is do nothing
        '''
        raw_text = query
        context_tokens = tokenizer.encode(raw_text)
        return raw_text, context_tokens

if __name__ == '__main__':
    pass

