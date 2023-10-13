import os
cur_dir = os.path.split(os.path.realpath(__file__))[0]
root_dir = os.path.abspath(os.path.dirname(cur_dir) + os.path.sep + "..")

import json
from typing import List, Literal, Optional
from dataclasses import dataclass, field

from loguru import logger


@dataclass
class EvaluateArguments:
    r"""
    Arguments
    """
    model_path: str = field(
        metadata={"help": "Path of the model and tokenizer"}
    )
    model_name: str = field(
        metadata={"help": "Name of the model, now support qwen, baichuan, ..."}
    )
    model_conf_path: str = field(
        default = root_dir + os.path.sep + 'conf' + os.path.sep + 'model_conf.json',
        metadata={"help": "Path of model's loader and context_builder class"}
    )
    eval_dataset_list: str = field(
        default = 'all',
        metadata={"help": "Which datasets to evaluate on. default is all datasets, if want to test on multiple datasets, use # as seperator"}
    )
    eval_dataset_type: str = field(
        default = 'test',
        metadata={"help": "Which type of datasets to evaluate on. default is test, must be one of (test, valid, dev)"}
    )
    eval_dataset_fp_conf_path: str = field(
        default = root_dir + os.path.sep + 'conf' + os.path.sep + 'dataset_fp.json',
        metadata={"help": "Path of dataset_name and filepath config file"}
    )
    k_shot: int = field(
        default = 0,
        metadata={"help": "k-shot test, k should be in (0, 1,2,3,4,5)"}
    )
    seed: int = field(
        default = 100,
        metadata={"help": "Random seed, default 100"}
    )
    data_path: str = field(
        default = '/mnt/llm/DevOpsEval/data/devopseval',
        metadata={'help': 'Path to the devopseval dataset'}
    )

    def init_for_training(self):
        self.eval_dataset_list = self.eval_dataset_list.split('#')
        if 'all' in self.eval_dataset_list:
            logger.info('Detecting all in eval_dataset_list, evaluating on all dataset')
            self.eval_dataset_list = ['all']
        
        assert self.eval_dataset_type in ('dev', 'test', 'val')
        assert self.k_shot in (0,1,2,3,4,5)