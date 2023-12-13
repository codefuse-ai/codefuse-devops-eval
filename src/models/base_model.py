# from vllm import LLM, SamplingParams
# from vllm.model_executor.parallel_utils.parallel_state import destroy_model_parallel


from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AutoTokenizer
from peft import PeftModel, PeftConfig

from .generate_configs import GenerateConfigs



class ToolModel:
    def __init__(self, model_path: str, template: str, trust_remote_code=True, tensor_parallel_size=1, gpu_memory_utilization=0.25):
        self.model_path = model_path
        self.trust_remote_code = trust_remote_code
        self.tensor_parallel_size = tensor_parallel_size
        self.gpu_memory_utilization = gpu_memory_utilization
        self.load_model(self.model_path, self.trust_remote_code, self.tensor_parallel_size, self.gpu_memory_utilization)

    def generate(self, prompts: str, template: str = None, generate_configs: GenerateConfigs = None) -> list:
        '''产出对应结果'''
        pass

    def generate_params(
        self, generate_configs: GenerateConfigs,
    ):
        '''generate param'''
        kargs = generate_configs.dict()
        return kargs
        
    def load_model(self, model_path, trust_remote_code=True, tensor_parallel_size=1, gpu_memory_utilization=0.25):
        '''加载模型'''
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=trust_remote_code)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path, device_map="auto", trust_remote_code=trust_remote_code).eval()

        # self.model = LLM(model=model_path, trust_remote_code=trust_remote_code, tensor_parallel_size=tensor_parallel_size, gpu_memory_utilization=gpu_memory_utilization)