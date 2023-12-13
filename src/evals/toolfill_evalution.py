from src.models.base_model import ToolModel
from src.models.generate_configs import GenerateConfigs
from src.datasets import ToolFillDataset
from .base_evalution import ToolEvalution



class ToolFillEvalution(ToolEvalution):
    def __init__(
        self, 
        model: ToolModel,
        dataset: ToolFillDataset,
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
        for idx, data in enumerate(self.dataset):
            prompt = self.base_prompt.format(**data)
            answer = data["api_param"]
            predict = self.generate(prompt, self.template, self.generate_configs)
            self.predicts.append({"prompt": prompt, "predict": predict, "answer": answer})
        
        metric = self.eval_metric(self.predicts)
        return metric
        
    def generate(self, prompt, template, generate_configs):
        '''返回结果'''
        return self.model.generate(prompt, template, generate_configs)
        
    def eval_metric(self, datas):
        ''''''
        self.right_predicts = []
        self.wrong_predicts = []
        self.error_predicts = []
        for data in datas:
            prompt, predict, answer = data["prompt"], data["predict"], data["answer"]
            
            try:
                predict_json = predict if isinstance(predict, dict) else eval(predict)
                answer_json = answer if isinstance(answer, dict) else eval(answer)
                if predict_json == answer_json:
                    # print("prompt: {}\npredict: {}\nanswer: {}".format(prompt, predict, answer))
                    self.right_predicts.append({"prompt": prompt, "predict": predict, "answer": answer})
                else:
                    self.wrong_predicts.append({"prompt": prompt, "predict": predict, "answer": answer})
            except:
                self.error_predicts.append({"prompt": prompt, "predict": predict, "answer": answer})
        # 
        print(len(self.right_predicts), len(self.wrong_predicts), len(self.error_predicts))

        metric = {
            "accuracy": len(self.right_predicts)/(len(self.right_predicts)+len(self.wrong_predicts)+len(self.error_predicts)),
            "error": len(self.error_predicts)/(len(self.right_predicts)+len(self.wrong_predicts)+len(self.error_predicts)),
        }
        return metric
