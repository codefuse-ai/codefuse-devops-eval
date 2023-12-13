from src.models.base_model import ToolModel
from src.models.generate_configs import GenerateConfigs
from src.datasets import ToolFillDataset



class ToolEvalution:
    def __init__(
        self, 
        model: ToolModel,
        dataset: ToolFillDataset,
        base_prompt: str = '',
        generate_configs: GenerateConfigs = None,
    ):
        self.model = model
        self.dataset = dataset
        self.base_prompt = base_prompt
        self.generate_configs = generate_configs
        
        if not isinstance(model, ToolModel):
            raise BaseException(f"must be ToolModel Class! not {model}")
            
    def calc(self):
        '''开始计算结果'''
        self.predicts = []
        for idx, data in enumerate(self.dataset):
            # if idx >= 5: break
            prompt = self.base_prompt.format(**data)
            answer = data["api_param"]
            predict = self.generate(prompt, self.generate_configs)
            self.predicts.append({"prompt": prompt, "predict": predict, "answer": answer})
        
        metric = self.eval_metric(self.predicts)
        return metric
        
    def generate(self, prompt, generate_configs):
        '''返回结果'''
        return self.model.generate(prompt, generate_configs)
    
    def eval_metric(self, datas):
        '''calc custom metric'''
        pass

