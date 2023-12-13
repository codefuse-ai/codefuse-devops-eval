import os
import re
import json
import random
import torch
import transformers
from transformers import AutoModelForCausalLM, CodeLlamaTokenizer, TextStreamer
end_token_id = 2
checkpoint = "/mnt/user/230854/output/vbase-llama-16k-hf/transformers"
print(checkpoint)
print("Loading model")
model = AutoModelForCausalLM.from_pretrained(checkpoint, device_map="auto").half().eval()
tokenizer = CodeLlamaTokenizer.from_pretrained(checkpoint)
print("Loading finish")
streamer = TextStreamer(tokenizer, skip_prompt=True)
torch.manual_seed(random.randint(0, 100000))
temperature = 0.2
top_p = 0.95
top_k = 40
repetition_penalty = 1.1
output_len = 2048
role_start = "[START]"
role_end = "[END]"


def change2chatml(fc_dict):
    chatrounds_list = []
    if fc_dict["chatrounds"][0]["role"] == "system":
        role = "system"
        content = fc_dict["chatrounds"][0]["content"]
        chatrounds_list.append({"role":role, "content":content})
    else:
        role = "system"
        content = "CodeFuse是一个面向研发领域的智能助手，旨在中立的、无害的帮助用户解决开发相关的问题，所有的回答均使用Markdown格式返回。\n你能利用许多工具和功能来完成给定的任务，在每一步中，你需要分析当前状态，并通过执行函数调用来确定下一步的行动方向。你可以进行多次尝试。如果你计划连续尝试不同的条件，请每次尝试一种条件。若给定了Finish函数,则以Finish调用结束，若没提供Finish函数，则以不带function_call的对话结束。"
        chatrounds_list.append({"role":role, "content":content})
    
    if fc_dict.get("functions",[]):
        role = "funcionapis"
        content = "You are ToolGPT, you have access to the following APIs:"
        content += json.dumps(fc_dict["functions"], ensure_ascii=False, sort_keys=True)
        chatrounds_list.append({"role":role, "content":content})

    for chat_dict in fc_dict["chatrounds"]:
        if chat_dict["role"] == "user":
            role = "human"
            content = chat_dict["content"]
            chatrounds_list.append({"role":role, "content":content})
        elif chat_dict["role"] == "assistant":
            role = "bot"
            if "function_call" in chat_dict:
                function_call_dict = {}
                function_call_dict["content"] = chat_dict["content"]
                function_call_dict["name"] = chat_dict["function_call"]["name"]
                function_call_dict["arguments"] = chat_dict["function_call"]["arguments"]
                content = "#function"+json.dumps(function_call_dict, ensure_ascii=False)
            else:
                content = chat_dict["content"]
            chatrounds_list.append({"role":role, "content":content})
        elif chat_dict["role"] == "function":
            role = "function"
            function_call_rst = {}
            function_call_rst["name"] = chat_dict["name"]
            function_call_rst["content"] = chat_dict["content"]
            content = json.dumps(function_call_rst, ensure_ascii=False)
            chatrounds_list.append({"role":role, "content":content})
    return chatrounds_list


def get_chatrounds_ids(chatrounds_list):
    input_ids  = []
    for chatround in chatrounds_list:
        input_ids += tokenizer.encode(role_start + chatround["role"]+ role_end) + tokenizer.encode(chatround["content"], add_special_tokens=False) + [tokenizer.eos_token_id]
    input_ids += tokenizer.encode(role_start + "bot" + role_end)
    return input_ids

class GetAssistantAns():
    # 按照自己推理需求自己修改代码

    def __init__(self):
        pass

    def gen_answer(self, chat_dict):
        chatrounds_list = change2chatml(chat_dict)
        input_ids = get_chatrounds_ids(chatrounds_list)
        output_ids = model.generate(torch.tensor([input_ids]).to(model.device), max_new_tokens=output_len, num_beams=1, num_return_sequences=1, do_sample=True, temperature=temperature, top_p=top_p, eos_token_id=end_token_id, top_k=top_k, streamer=None, repetition_penalty=repetition_penalty, pad_token_id=10000)[0]
        res = tokenizer.decode(output_ids[len(input_ids):-1])
        save_dict = {"role": "assistant"}
        if res.startswith("#function"):
            try:
                res_dict = json.loads(re.sub("^#function", "", res))
                save_dict["content"] = res_dict["content"]
                save_dict["function_call"] = {}
                save_dict["function_call"]["name"] = res_dict["name"]
                save_dict["function_call"]["arguments"] = res_dict["arguments"]
            except Exception as e:
                print(e)
                save_dict = {"role": "assistant"}
                save_dict["content"] = res
        else:
            save_dict["content"] = res
        
        print(save_dict)

        return save_dict
