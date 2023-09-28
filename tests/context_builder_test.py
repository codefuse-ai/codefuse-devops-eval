import sys
sys.path.append('/mnt/llm/DevOpsEval')

from loguru import logger

from src.context_builder.context_builder_family import QwenContextBuilder
from src.model_and_tokenizer_loader.model_and_tokenizer_loader_family import QwenModelAndTokenizerLoader


if __name__ == '__main__':
    query = '你好'
    system = '请帮助我'
    tokenizer_path = '/mnt/llm/devopspal/model/Qwen-7B'

    model_path = '/mnt/llm/devopspal/model/Qwen-7B'
    qwen_model_loader = QwenModelAndTokenizerLoader()
    tokenizer = qwen_model_loader.load_tokenizer(model_path)

    qcb = QwenContextBuilder()
    a, b = qcb.make_context(tokenizer, query, system)
    logger.debug(a)
    logger.debug(b)
