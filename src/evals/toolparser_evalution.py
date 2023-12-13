from src.models.base_model import ToolModel
from src.models.generate_configs import GenerateConfigs
from src.datasets import ToolParserDataset
from .base_evalution import ToolEvalution
from .utils import rec_search_key


class ToolParserEvalution(ToolEvalution):
    def __init__(
        self, 
        model: ToolModel,
        dataset: ToolParserDataset,
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
            # if idx >= 5: break
            prompt = self.base_prompt.format(**data)
            response = data["response"]
            answer = data["selected_keys"]
            predict = self.generate(prompt, self.template, self.generate_configs)
            self.predicts.append({"prompt": prompt, "predict": predict, "answer": answer, "response": response})
        
        metric = self.eval_metric(self.predicts)
        return metric
        
        self.model = model
        self.dataset = dataset
        self.base_prompt = base_prompt
        self.template = template
        self.generate_configs = generate_configs
        
        if not isinstance(model, ToolModel):
            raise BaseException(f"must be ToolModel Class! not {model}")
            
    def generate(self, prompt, template, generate_configs):
        '''返回结果'''
        return self.model.generate(prompt, template, generate_configs)
        
    def eval_metric(self, datas):
        ''''''
        self.right_predicts = []
        self.wrong_predicts = []
        self.error_predicts = []
        for data in datas:
            prompt, predict, answer, response = data["prompt"], data["predict"], data["answer"], data["response"]
            selected_keys = rec_search_key(response, "", [], predict)
            try:
                predict_json = selected_keys if isinstance(selected_keys, list) else eval(selected_keys)
                answer_json = answer if isinstance(answer, list) else eval(answer)
                
                predict_json = set(predict_json) if isinstance(predict_json, list) else predict_json
                answer_json = set(answer_json) if isinstance(answer_json, list) else answer_json

                if predict_json == answer_json:
                    # print("prompt: {}\npredict: {}\nanswer: {}".format(prompt, predict, answer))
                    self.right_predicts.append({"prompt": prompt, "predict": predict, "answer": answer, "response": response})
                else:
                    self.wrong_predicts.append({"prompt": prompt, "predict": predict, "answer": answer, "response": response})
            except:
                self.error_predicts.append({"prompt": prompt, "predict": predict, "answer": answer, "response": response})
        # 
        print(len(self.right_predicts), len(self.wrong_predicts), len(self.error_predicts))

        metric = {
            "accuracy": len(self.right_predicts)/(len(self.right_predicts)+len(self.wrong_predicts)+len(self.error_predicts)),
            "error": len(self.error_predicts)/(len(self.right_predicts)+len(self.wrong_predicts)+len(self.error_predicts)),
        }
        return metric
