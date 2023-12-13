# from vllm import LLM, SamplingParams
# from vllm.model_executor.parallel_utils.parallel_state import destroy_model_parallel


from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AutoTokenizer
from peft import PeftModel, PeftConfig

from .generate_configs import GenerateConfigs
from .base_model import ToolModel



class QwenModel(ToolModel):
    def __init__(self, model_path: str, peft_path: str = None, template: str = "default", trust_remote_code=True, tensor_parallel_size=1, gpu_memory_utilization=0.25):
        self.model_path = model_path
        self.peft_path = peft_path
        self.template = template
        self.trust_remote_code = trust_remote_code
        self.tensor_parallel_size = tensor_parallel_size
        self.gpu_memory_utilization = gpu_memory_utilization
        self.load_model(self.model_path, self.peft_path, self.trust_remote_code, self.tensor_parallel_size, self.gpu_memory_utilization)

    def generate(
        self, prompts: str, 
        template: str = None,
        generate_configs: GenerateConfigs =None,
        history: list = None,
    ) -> list:
        '''产出对应结果'''
        template = self.template if template is None else template

        params = self.generate_params(generate_configs)

        if template == "default":
            inputs = self.tokenizer(prompts, return_tensors="pt")
            inputs["input_ids"] = inputs["input_ids"].cuda()

            inputs.update(params)
            output = self.model.generate(**inputs)
            predict = self.tokenizer.decode(output[0].tolist())[len(prompts):]
            predict = predict.replace("<|endoftext|>", "").replace("</s>",  "")
            return predict
        elif template != "default":
            output, _ = self.model.chat(self.tokenizer, prompts, history=history, **params)
            return output
        # params = self.generate_params(generate_configs)
        # sampling_params = SamplingParams(**params)
        # prompts = [prompts] if isinstance(prompts, str) else prompts
        # outputs = self.model.generate(prompts, sampling_params)
        # return [i.outputs[0].text for i in outputs]

    def generate_params(
        self, generate_configs: GenerateConfigs,
    ):
        '''generate param'''
        kargs = generate_configs.dict()
        params = {
                    "max_new_tokens": kargs.get("max_new_tokens", 128),
                    "top_k": kargs.get("top_k", 50),
                    "top_p": kargs.get("top_p", 0.95),
                    "temperature": kargs.get("temperature", 1.0),
        }
        
        # params = {
        #             "n": 1,
        #             "max_tokens": kargs.get("max_new_tokens", 128),
        #             "best_of": kargs.get("beam_bums", 1), 
        #             "top_k": kargs.get("top_k", 50),
        #             "top_p": kargs.get("top_p", 0.95),
        #             "temperature": kargs.get("temperature", 1.0),
        #             "length_penalty": kargs.get("length_penalty", 1.0),
        #             "presence_penalty": kargs.get("presence_penalty", 1.0), 
        #             "stop": kargs.get("stop_words", ["<|endoftext|>"]),
        # }
        return params
        
    def load_model(self, model_path, peft_path=None, trust_remote_code=True, tensor_parallel_size=1, gpu_memory_utilization=0.25):
        '''加载模型'''
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=trust_remote_code)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path, device_map="auto", trust_remote_code=trust_remote_code).eval()
        if peft_path:
            self.model = PeftModel.from_pretrained(self.model, peft_path)

        # self.model = LLM(model=model_path, trust_remote_code=trust_remote_code, tensor_parallel_size=tensor_parallel_size, gpu_memory_utilization=gpu_memory_utilization)