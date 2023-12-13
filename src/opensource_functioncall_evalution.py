#!/usr/bin/python
# -*- coding: utf-8 -*-

############################################
# File: opensource_functioncall_evalution.py
# create by youmi
# Time: 2023-11-23 13:10
############################################


import os
import sys
import random
import time
import shutil
import json
import jieba
import re
import copy
import numpy as np
from tqdm import tqdm
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from getAssistantAns import GetAssistantAns


test_ans_file_list = [
        "fcdata_zh_test.jsonl"
        ]

# 多进程评测加速
GPU_NUM = 1

# function call 回复测试总数
function_call_sum = 0
# function call 回复正确数
function_call_correct = 0
# function call 回复失败数
function_call_fail = 0
# function call 回复失败中，本应该调用工具但是模型没有调用， 无工具识别识别错误数
function_call_fail_functioncall = 0
# function call 回复失败数中，因为函数名不对导致的失败数, 这部分包括模型幻觉出错
function_call_fail_name = 0
# function call 回复失败数中，工具名对了，但是参数不对导致的失败数
function_call_fail_param = 0
# function call 回复失败中 函数名幻觉的失败数
function_call_fail_name_illusion = 0

# assistant ans 回复相关度列表
assistant_ans_relevancy_list = []

# 推理结果
test_result_lines = [] 

get_assistant_ans = GetAssistantAns(gpu_num=GPU_NUM)

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


# 计算两个答案的相关度
# 要是预测回复的是functioncall类型的，相似为0
# 要是预测回复的包含了所有要点，相似度为1
# 相似度保存在assistant_ans_relevancy_list中
def calc_relevancy(ass_predict, ass_truth, chatrounds):
    global assistant_ans_relevancy_list
    if "function_call" in ass_predict:
        assistant_ans_relevancy_list.append(0)
        return
    # 将user 和 function 的部分组合
    content_msg = ""
    for chatround in chatrounds["chatrounds"]:
        if chatround["role"] == "user":
            content_msg += chatround["content"]
        elif chatround["role"] == "function":
            content_msg += chatround["content"]
    content_msg_counter = Counter(jieba.cut(remove_punctuation(content_msg)))
    ass_truth_counter = Counter(jieba.cut(remove_punctuation(ass_truth["content"])))
    ass_predict_counter = Counter(jieba.cut(remove_punctuation(ass_predict["content"])))
    relative_counter = content_msg_counter & ass_truth_counter
    len_relative = sum(relative_counter.values())
    predict_relative = ass_predict_counter & relative_counter

    if len_relative == 0:
        # 要是标准答案和问题相关词都无 直接给1
        assistant_ans_relevancy_list.append(1)
    else:
        # 交集与相关词的占比
        assistant_ans_relevancy_list.append(sum(predict_relative.values())/len_relative)




def calc_llm_index(ass_predict, ass_truth, chatrounds):
    global function_call_sum, function_call_correct, function_call_fail, function_call_fail_functioncall, function_call_fail_name, function_call_fail_name_illusion, function_call_fail_param

    chatrounds_functionname_list = []
    for function_dict in chatrounds.get("functions", []):
        chatrounds_functionname_list.append(function_dict["name"])

    if "function_call" in ass_truth:
        function_call_sum += 1
        if "function_call" not in ass_predict:
            function_call_fail += 1
            function_call_fail_functioncall += 1
        elif ass_predict["function_call"]["name"] not in chatrounds_functionname_list:
            # 模型幻觉
            function_call_fail += 1
            function_call_fail_name  += 1
            function_call_fail_name_illusion += 1
        else:
            function_call_name_label = False
            function_call_args_label = False
            if ass_predict["function_call"]["name"] == ass_truth["function_call"]["name"]:
                function_call_name_label = True
                if cmp_arguments(ass_predict["function_call"]["arguments"], ass_truth["function_call"]["arguments"]):
                    function_call_args_label = True
                else:
                    function_call_fail_param += 1
            else:
                function_call_fail_name += 1

            if function_call_name_label and function_call_args_label:
                function_call_correct += 1
            else:
                function_call_fail += 1
    else:
        calc_relevancy(ass_predict, ass_truth, chatrounds)


def print_result():
    # 打印指标结果
    print("=============统计数据=========================")
    print(f"function_call_sum: {function_call_sum}")
    print(f"function_call_correct: {function_call_correct}")
    print(f"function_call_fail: {function_call_fail}")
    print(f"function_call_fail_functioncall: {function_call_fail_functioncall}")
    print(f"function_call_fail_name: {function_call_fail_name}")
    print(f"function_call_fail_param: {function_call_fail_param}")
    print(f"function_call_fail_name_illusion: {function_call_fail_name_illusion}")
    print(f"assistant_ans_sum: {len(assistant_ans_relevancy_list)}")
    print(f"assistant_ans_relevancy: {np.mean(assistant_ans_relevancy_list)}")
    print("=============实验结果=========================")
    function_call_correct_rate = function_call_correct/function_call_sum
    function_call_fail_rate = function_call_fail/function_call_sum
    function_call_fail_functioncall_rate = function_call_fail_functioncall/function_call_fail if function_call_fail else 0
    function_call_fail_name_rate = function_call_fail_name/function_call_fail if function_call_fail else 0
    function_call_fail_param_rate = function_call_fail_param/function_call_fail if function_call_fail else 0
    function_call_fail_name_illusion_rate = function_call_fail_name_illusion/function_call_fail if function_call_fail else 0
    print(f"工具识别正确率fccr: {function_call_correct_rate}")
    print(f"工具识别失败率fcfr: {function_call_fail_rate}")
    print(f"工具调用识别失败占比fcffr: {function_call_fail_functioncall_rate}")
    print(f"工具名识别失败占比fcfnr: {function_call_fail_name_rate}")
    print(f"工具参数识别失败占比fcfpr: {function_call_fail_param_rate}")
    print(f"工具幻觉识别失败占比fcfnir: {function_call_fail_name_illusion_rate}")
    print(f"助手回复答案相关度aar: {np.mean(assistant_ans_relevancy_list)}")
    print("==============================================")
    # 保存数据
    with open("test_result_data.jsonl","w") as fw:
        for line in test_result_lines:
            print(line, file=fw)


def test_process(test_lines, gpu_index):
    global test_result_lines
    for line in tqdm(test_lines, desc="Process%02d"%(gpu_index)):
        chat_dict = json.loads(line)
        test_dict = {}
        test_dict["functions"] = chat_dict["functions"]
        test_dict["chatrounds"] = []
        for chatround in chat_dict["chatrounds"]:
            if chatround["role"] == "assistant":
                ass_predict = get_assistant_ans.gen_answer(test_dict, gpu_index=gpu_index)
                save_dict = copy.deepcopy(test_dict)
                save_dict["chatrounds"].append(ass_predict)
                test_result_lines.append(json.dumps(save_dict, ensure_ascii=False))
                calc_llm_index(ass_predict, chatround, test_dict)
            test_dict["chatrounds"].append(chatround)


def main():
    pool = ThreadPoolExecutor(max_workers=GPU_NUM)

    test_lines = []
    for test_ans_file in test_ans_file_list:
        print(test_ans_file)
        with open(test_ans_file, "r") as f:
            lines = f.readlines()
            test_lines += lines

    batch_num = len(test_lines)//GPU_NUM + int(len(test_lines)%GPU_NUM>0)

    obj_list = []
    for idx in range(GPU_NUM):
        batch_test_lines = test_lines[idx*batch_num:(idx+1)*batch_num]
        obj = pool.submit(test_process, batch_test_lines, gpu_index=idx)
        obj_list.append(obj)

    for future in as_completed(obj_list):
        # 暂时留在这里，但是其实没有返回数据
        data = future.result()

    print_result()

if __name__ == "__main__":
    main()
