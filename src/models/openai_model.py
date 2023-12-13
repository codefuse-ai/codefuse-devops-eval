# from vllm import LLM, SamplingParams
# from vllm.model_executor.parallel_utils.parallel_state import destroy_model_parallel


from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AutoTokenizer
from peft import PeftModel, PeftConfig

from .generate_configs import GenerateConfigs
from .base_model import ToolModel

import openai, os



class OpenaiModel(ToolModel):
    def __init__(self, model_path: str, template: str, system_prompt):
        self.model_path = model_path
        self.template = template
        self.system_prompt = system_prompt

    def generate(
        self, prompts: str, template: str = None,
        generate_configs: GenerateConfigs =None,
    ) -> list:
        '''产出对应结果'''
        template = self.template if template is None else template

        params = self.generate_params(generate_configs)

        messages = [{"role": "system", "content": self.system_prompt}, {"role": "user", "content": prompts}]
        try:
            result = openai.ChatCompletion.create(api_base=os.environ["OPENAI_API_BASE"], api_key=os.environ["OPENAI_API_KEY"], model=self.model_path, messages=messages, **params)
        # print("prompt_tokens: {}, completion_tokens: {}".format(result["usage"]["prompt_tokens"], result["usage"]["completion_tokens"]))
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            result = str(e)

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
        return params

