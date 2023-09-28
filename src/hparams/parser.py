import sys
sys.path.append('/mnt/llm/DevOpsEval')

from loguru import logger
from transformers import HfArgumentParser
from src.hparams.evaluate_args import EvaluateArguments


def get_all_args(
    args = None
) -> EvaluateArguments:
    parser = HfArgumentParser((
        EvaluateArguments
    ))
    eval_args = parser.parse_args_into_dataclasses(args)[0]
    eval_args.init_for_training()
    return eval_args


if __name__ == '__main__':
    a = get_all_args()
    logger.debug(a)