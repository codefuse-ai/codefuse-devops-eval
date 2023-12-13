from src.models.base_model import ToolModel
from src.models.generate_configs import GenerateConfigs
from src.datasets import FuncCallDataset
from src.utils.jsonl_utils import read_jsonl_file
from .base_evalution import ToolEvalution

from collections import Counter
import jieba, re, json, os
import numpy as np
from loguru import logger


def remove_punctuation(text):
    pattern = r'[^\w\s]'
    return re.sub(pattern, '', text)


def cmp_arguments(args_str1, args_str2):
    rtn_flag = False
    try:
        args_dict1 = json.loads(args_str1)
        args_dict2 = json.loads(args_str2)
        # 比较两个字典是否一致
        if args_dict1 == args_dict2:
            rtn_flag = True
    except Exception as e:
        print("json.loads error: ", e)
        return rtn_flag
    return rtn_flag


class FuncCallEvalution(ToolEvalution):
    def __init__(
        self, 
        model: ToolModel,
        dataset: FuncCallDataset,
        base_prompt: str = '',
        template: str = 'default',
        generate_configs: GenerateConfigs = None,
    ):
        self.model = model
        self.dataset = dataset
        self.base_prompt = base_prompt
        self.template = template
        self.generate_configs = generate_configs
        
        if not isinstance(model, ToolModel):
            raise BaseException(f"must be ToolModel Class! not {model}")
            
    def calc(self):
        '''开始计算结果'''
        self.predicts = []
        func_call_train_datas = self.create_prompts(self.dataset)

        for idx, data in enumerate(func_call_train_datas):
            print(f"总共 {len(func_call_train_datas)} 条prompt，当前运行到第 {idx} 条prompt", end="\r")
            prompt = data["instruction"]
            history = data["history"]
            answer = data["output"]
            functions = data["functions"]
            predict = self.generate(prompt, self.template, self.generate_configs, history)

            if "arguments" in answer:
                answer = {"content": answer["content"], "function_call": {"name": answer["name"], "arguments": answer["arguments"]}}

            if "#function" in predict:
                try:
                    predict_param = json.loads(predict.split("#function")[-1])
                    if "arguments" in predict_param:
                        predict_param = {
                            "content": predict_param["content"], 
                            "function_call": {"name": predict_param["name"], "arguments": predict_param["arguments"]}
                        }
                    predict = {**predict_param, **{"role": "assistant"}}
                except Exception as e:
                    logger.error("content: {content}")
                    predict = {**{"content": predict_param}, **{"role": "assistant"}}
            else:
                predict =  {
                        "role": "assistant",
                        "content": predict
                    }

            self.predicts.append({
                "prompt": prompt, "history": history, 
                "predict": predict, "answer": answer,
                "functions": functions
                })
        
        metric = self.eval_metric(self.predicts)
        return metric

    def calc_from_predicts(self, file_path):
        if os.path.exists(file_path):
            self.predicts = read_jsonl_file(file_path)
            metric = self.eval_metric(self.predicts)
            return metric
        else:
            return self.calc()
    
    def create_prompts(self, func_call_datas):
        system_content = '''CodeFuse是一个面向研发领域的智能助手，旨在中立的、无害的帮助用户解决开发相关的问题，所有的回答均使用Markdown格式返回。
        你能利用许多工具和功能来完成给定的任务，在每一步中，你需要分析当前状态，并通过执行函数调用来确定下一步的行动方向。你可以进行多次尝试。如果你计划连续尝试不同的条件，请每次尝试一种条件。若给定了Finish函数,则以Finish调用结束，若没提供Finish函数，则以不带function_call的对话结束。'''
        function_format = '''You are ToolGPT, you have access to the following APIs:\n{tools}'''

        func_call_train_datas = []
        history_error_cnt = 0
        funccall_error_cnt = 0

        for data in func_call_datas:
            tools = data["functions"]
            chatrounds = data["chatrounds"]

            function_content = ""
            if len(tools) > 0:
                function_content = function_format.format(tools=json.dumps(tools, ensure_ascii=False, sort_keys=True))

            history = []
            for i in chatrounds:
                if i["role"]=="system":
                    continue

                if i["role"]=="user":
                    history.append(("user", i["content"]))

                if i["role"] == "assistant":
                    if "function_call" in i:
                        if not isinstance(i["function_call"], dict):
                            funccall_error_cnt+=1
                            continue
                        content  = "#function" + json.dumps({**{"content": i["content"]}, **i["function_call"]}, ensure_ascii=False)
                    else:
                        content = i["content"]
                    history.append(("assistant", content))
                                            
                    
                if i["role"] == "function":
                    content  = json.dumps({**{"content": i["content"]}, **{"name": i["name"]}}, ensure_ascii=False)
                    history.append(("user", content))
                
            
            history = [i[1] for i in history]
            history[0] = "\n".join([system_content,function_content, history[0]])
            
            for his_idx in range(0, len(history), 2):
                output = history[his_idx+1]

                if "#function" in output:
                    output = output.split("#function")[-1]

                try:
                    output = json.loads(output)
                except:
                    output = {"content": output}


                func_call_train_datas.append(
                    {
                        "instruction": history[his_idx], 
                        "input": "",
                        "output": output, 
                        "history": [history[:his_idx+2][i:i+2] for i in range(0, len(history[:his_idx]), 2)],
                        "functions": tools
                    },
                )
        return func_call_train_datas

    def generate(self, prompt, template, generate_configs, history=None):
        '''返回结果'''
        return self.model.generate(prompt, template, generate_configs, history)
        
    def eval_metric(self, datas):
        ''''''
        # function call 回复测试总数
        self.function_call_sum = 0
        # function call 回复正确数
        self.function_call_correct = 0
        # function call 回复失败数
        self.function_call_fail = 0
        # function call 回复失败中，本应该调用工具但是模型没有调用， 无工具识别识别错误数
        self.function_call_fail_functioncall = 0
        # function call 回复失败数中，因为函数名不对导致的失败数
        self.function_call_fail_name = 0
        # function call 回复失败数中，因为参数不对导致的失败数
        self.function_call_fail_param = 0
        # function call 回复失败中 函数名幻觉的失败数
        self.function_call_fail_name_illusion = 0

        # assistant ans 回复相关度列表
        self.assistant_ans_relevancy_list = []

        for data in datas:
            ass_predict = data["predict"]
            ass_truth = data["answer"]
            functions = data["functions"]
            history = data["history"]
            # 将user 和 function 的部分组合
            content_msg = ""
            for user_msg, assistant_msg in history:
                content_msg += user_msg

            # if "#function" in ass_truth:
            if "function_call" in ass_truth:
                self.calc_func_params(ass_predict, ass_truth, functions)
            else:
                self.calc_relevancy(ass_predict, ass_truth, content_msg)

        self.print_result()
        return {
            "function_call_correct_rate": self.function_call_correct_rate,
            "function_call_fail_rate": self.function_call_fail_rate,
            "function_call_fail_functioncall_rate": self.function_call_fail_functioncall_rate,
            "function_call_fail_name_rate": self.function_call_fail_name_rate,
            "function_call_fail_param_rate": self.function_call_fail_param_rate,
            "function_call_fail_name_illusion_rate": self.function_call_fail_name_illusion_rate
            }

    def calc_func_params(self, ass_predict, ass_truth, functions):
        self.function_call_sum += 1

        function_names = [i["name"] for i in functions]
        # ass_predict_param = json.loads(ass_predict.split("#function")[-1])
        # ass_truth_param = json.loads(ass_truth.split("#function")[-1])

        if "function_call" not in ass_predict:
            self.function_call_fail += 1
            self.function_call_fail_functioncall += 1
        elif ass_predict["function_call"]["name"] not in function_names:
            # 模型幻觉
            self.function_call_fail += 1
            self.function_call_fail_name  += 1
            self.function_call_fail_name_illusion += 1
        else:
            function_call_name_label = False
            function_call_args_label = False
            if ass_predict["function_call"]["name"] == ass_truth["function_call"]["name"]:
                function_call_name_label = True
                if cmp_arguments(ass_predict["function_call"]["arguments"], ass_truth["function_call"]["arguments"]):
                    function_call_args_label = True
                else:
                    self.function_call_fail_param += 1
            else:
                self.function_call_fail_name += 1
            # # 是否可能存在名字错误参数正确的情况？
            # if self.cmp_arguments(ass_predict["function_call"]["arguments"], ass_truth["function_call"]["arguments"]):
            #     function_call_args_label = True
            # else:
            #     self.function_call_fail_param += 1

            if function_call_name_label and function_call_args_label:
                self.function_call_correct += 1
            else:
                self.function_call_fail += 1

    def calc_relevancy(self, ass_predict, ass_truth, content_msg):
        if "function_call" in ass_predict:
            self.assistant_ans_relevancy_list.append(0)
            return

        content_msg_counter = Counter(jieba.cut(remove_punctuation(content_msg)))
        ass_truth_counter = Counter(jieba.cut(remove_punctuation(ass_truth["content"])))
        ass_predict_counter = Counter(jieba.cut(remove_punctuation(ass_predict["content"])))
        relative_counter = content_msg_counter & ass_truth_counter
        len_relative = sum(relative_counter.values())
        predict_relative = ass_predict_counter & relative_counter

        if len_relative == 0:
            # 要是标准答案和问题相关词都无 直接给1
            self.assistant_ans_relevancy_list.append(1)
        else:
            # 交集与相关词的占比
            self.assistant_ans_relevancy_list.append(sum(predict_relative.values())/len_relative)

    def print_result(self, ):
        # 打印指标结果
        print("=============统计数据=========================")
        print(f"function_call_sum: {self.function_call_sum}")
        print(f"function_call_correct: {self.function_call_correct}")
        print(f"function_call_fail: {self.function_call_fail}")
        print(f"function_call_fail_name: {self.function_call_fail_name}")
        print(f"function_call_fail_param: {self.function_call_fail_param}")
        print(f"function_call_fail_name_illusion: {self.function_call_fail_name_illusion}")
        print(f"assistant_ans_sum: {len(self.assistant_ans_relevancy_list)}")
        print(f"assistant_ans_relevancy: {np.mean(self.assistant_ans_relevancy_list)}")
        print("=============实验结果=========================")
        self.function_call_correct_rate = self.function_call_correct/self.function_call_sum
        self.function_call_fail_rate = self.function_call_fail/self.function_call_sum
        self.function_call_fail_functioncall_rate = self.function_call_fail_functioncall/self.function_call_sum
        self.function_call_fail_name_rate = self.function_call_fail_name/self.function_call_sum
        self.function_call_fail_param_rate = self.function_call_fail_param/self.function_call_sum
        self.function_call_fail_name_illusion_rate = self.function_call_fail_name_illusion/self.function_call_sum

        # self.function_call_fail_functioncall_rate = self.function_call_fail_functioncall/self.function_call_fail if self.function_call_fail else 0
        # self.function_call_fail_name_rate = self.function_call_fail_name/self.function_call_fail if self.function_call_fail else 0
        # self.function_call_fail_param_rate = self.function_call_fail_param/self.function_call_fail if self.function_call_fail else 0
        # self.function_call_fail_name_illusion_rate = self.function_call_fail_name_illusion/self.function_call_fail if self.function_call_fail else 0
        print(f"工具识别正确率fccr: {self.function_call_correct_rate}")
        print(f"工具识别失败率fcfr: {self.function_call_fail_rate}")
        print(f"工具调用识别失败占比fcffr: {self.function_call_fail_functioncall_rate}")
        print(f"工具名识别失败占比fcfnr: {self.function_call_fail_name_rate}")
        print(f"工具参数识别失败占比fcfpr: {self.function_call_fail_param_rate}")
        print(f"工具幻觉识别失败占比fcfnir: {self.function_call_fail_name_illusion_rate}")
        print(f"助手回复答案相关度aar: {np.mean(self.assistant_ans_relevancy_list)}")
        print("==============================================")
