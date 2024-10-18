import os, sys

from src.datasets import ToolFillDataset, ToolParserDataset, ToolSummaryDataset, FuncCallDataset
from src.evals import ToolFillEvalution, ToolParserEvalution, ToolSummaryEvalution, FuncCallEvalution
from src.models import QwenModel, ToolModel, InternlmModel
from src.models.generate_configs import GenerateConfigs
from src.prompts.base_prompts_config import TOOL_FILL_BASE_PROMPT, TOOL_PARSER_BASE_PROMPT, TOOL_SUMMARY_BASE_PROMPT
from src.utils.jsonl_utils import save_to_jsonl_file

import warnings
import re

# 定义要过滤的警告消息内容
filtered_content = "for open-end generation"
# 过滤包含特定内容的警告消息
warnings.filterwarnings("ignore", message=re.escape(filtered_content))


model_infos = [
    {"model_name": "", "template": "chatml", "model_path": "",
     "peft_path": "", "model_class": QwenModel}]

datainfos = [
    {"dataset_path": "~/fcdata_luban_zh_test.jsonl", "dataset_name": "fcdata_luban_zh", "tool_task": "func_call"},
    {"dataset_path": "~/test_datas/fcdata_zh_test_v1.jsonl", "dataset_name": "fcdata_zh", "tool_task": "func_call"},
]

save_path = ""


for model_info in model_infos:
    print(f"******** model_name: {model_info['model_name']} *****")
    model_path = model_info["model_path"]
    peft_path = model_info["peft_path"]
    template = model_info["template"]

    tool_model = model_info["model_class"](model_path, peft_path, template, trust_remote_code=True, tensor_parallel_size=1, gpu_memory_utilization=0.25)

    for datainfo in datainfos:

        print(f"******** dataset_name: {datainfo['dataset_name']} *****")

        dataset_name = datainfo["dataset_name"]
        tool_task = datainfo["tool_task"]
        dataset_path = datainfo["dataset_path"]
        funccall_dataset = FuncCallDataset(dataset_name, tool_task, dataset_path)

        generate_configs = GenerateConfigs(max_new_tokens=256, temperature=0.2, stop_words=["<|endoftext|>"])

        funccall_evalution = FuncCallEvalution(
                    model=tool_model,
                    dataset=funccall_dataset,
                    base_prompt=TOOL_FILL_BASE_PROMPT,
                    template=model_info["template"],
                    generate_configs=generate_configs,
                )
        metric = funccall_evalution.calc()

        # save predict results to local
        save_to_jsonl_file(funccall_evalution.predicts, f"{save_path}/{model_info['model_name']}/{datainfo['dataset_name']}/result.jsonl")