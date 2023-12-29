import os
import json
import random
import torch
from transformers import AutoModelForCausalLM

class GetAssistantAns():
    # 按照自己推理需求自己修改代码

    def __init__(self, gpu_num=1):
        model = AutoModelForCausalLM.from_pretrained(model_name)
        device_list = []
        for gpu_idx in range(gpu_num):
            device_list.append(torch.device("cuda:0"))

        # 将模型移动到指定的GPU设备
        model.to(device)


    def gen_answer(self, chat_dict, gpu_index):
        # 这里实际根据自己推理逻辑 然后转为标准格式返回
        # 以下仅仅是样例
        import time
        print(os.environ["CUDA_VISIBLE_DEVICES"])
        time.sleep(1)
        rtn_dict1 = {
                "role": "assistant",
                "content": None,
                "function_call":
                {
                    "name": "get_fudan_university_scoreline",
                    "arguments": "{\n  \"year\": \"2020\"\n}"
                }
            }

        rtn_dict2 =  {
                "role": "assistant",
                "content": "2020年复旦大学的分数线如下：\n\n- 文科一批：630分\n- 文科二批：610分\n- 理科一批：650分\n- 理科二批：630分"
            }

        return random.choice([rtn_dict1, rtn_dict2])

# ======================================================================
# 下面注释的部分是一个huggingface推理的多卡的demo
# 备注 线程数量==2，也就是2卡效率最高 多个卡并不会提升效率，存在资源抢占的情况
# 可以采用多卡部署服务，然后调用服务的方式提升效率 

# import os
# import re
# import json
# import random
# import torch
# import copy
# import transformers
# from transformers import AutoModelForCausalLM, CodeLlamaTokenizer, TextStreamer
# end_token_id = 2
# checkpoint = "<your_huggingface_model_dir>"
# tokenizer = CodeLlamaTokenizer.from_pretrained(checkpoint)
# torch.manual_seed(random.randint(0, 100000))
# temperature = 0.2
# top_p = 0.95
# top_k = 40
# repetition_penalty = 1.1
# output_len = 2048
# role_start = "[START]"
# role_end = "[END]"


# def change2traindata(fc_dict):
#     chatrounds_list = []
#     # insert your code
#     # eg
#     # chatrounds_list = [
#     #     {
#     #         "role": "system",
#     #         "content":"你好，我是小助手，我能帮你做什么呢？"
#     #     },
#     #     {
#     #         "role": "functionapis"
#     #         "content": "You are tool gpt, you can using following apis []"
#     #     },
#     #     {
#     #         "role": "user",
#     #         "content": "我想知道复旦大学的分数线"
#     #     },
#     #     {
#     #         "role": "bot",
#     #         "content": "#function{*****}"
#     #     },
#     #     {
#     #         "role": "function",
#     #         "content": ******
#     #     },
#     #     {
#     #         "role": "bot",
#     #         "content": "复旦大学分数线640"
#     #     }
#     # ]
#     return chatrounds_list


# def get_chatrounds_ids(chatrounds_list):
#     input_ids  = []
#     for chatround in chatrounds_list:
#         input_ids += tokenizer.encode(role_start + chatround["role"]+ role_end) + tokenizer.encode(chatround["content"], add_special_tokens=False) + [tokenizer.eos_token_id]
#     input_ids += tokenizer.encode(role_start + "bot" + role_end)
#     return input_ids


# class GetAssistantAns():
#     # 按照自己推理需求自己修改代码

#     def __init__(self, gpu_num=1):
#         print(checkpoint)
#         print("Loading model")
#         model = AutoModelForCausalLM.from_pretrained(checkpoint).half().eval()
#         device_list = [torch.device(f"cuda:%d"%(i)) for i in range(gpu_num)]
#         self.model_list = [copy.deepcopy(model.to(device)) for device in device_list]
#         print("Loading finish")

#     def gen_answer(self, chat_dict, gpu_index=0):
#         chatrounds_list = change2traindata(chat_dict)
#         input_ids = get_chatrounds_ids(chatrounds_list)
#         output_ids = self.model_list[gpu_index].generate(torch.tensor([input_ids]).to(self.model_list[gpu_index].device), max_new_tokens=output_len, num_beams=1, num_return_sequences=1, do_sample=True, temperature=temperature, top_p=top_p, eos_token_id=end_token_id, top_k=top_k, streamer=None, repetition_penalty=repetition_penalty, pad_token_id=10000)[0]
#         res = tokenizer.decode(output_ids[len(input_ids):-1])
#         save_dict = {"role": "assistant"}
#         if res.startswith("#function"):
#             try:
#                 res_dict = json.loads(re.sub("^#function", "", res))
#                 save_dict["content"] = res_dict["content"]
#                 save_dict["function_call"] = {}
#                 save_dict["function_call"]["name"] = res_dict["name"]
#                 save_dict["function_call"]["arguments"] = res_dict["arguments"]
#             except Exception as e:
#                 print(e)
#                 save_dict = {"role": "assistant"}
#                 save_dict["content"] = res
#         else:
#             save_dict["content"] = res
#         # print(save_dict)
#         return save_dict
