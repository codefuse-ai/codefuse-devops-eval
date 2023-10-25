## 数据集评测教程

## 🚀 如何进行测试
如果需要在自己的 huggingface 格式的模型上进行测试的话，总的步骤分为如下几步:
1. 编写 Model 的 loader 函数
2. 编写 Model 的 context_builder 函数
3. 注册模型到配置文件中
4. 执行测试脚本
如果模型在加载进来后不需要特殊的处理，而且输入也不需要转换为特定的格式（e.g. chatml 格式或者其他的 human-bot 格式），请直接跳转到第四步直接发起测试。

#### 1. 编写 loader 函数
如果模型在加载进来还需要做一些额外的处理（e.g. tokenizer 调整），需要去 `src.context_builder.context_builder_family.py` 中继承 `ModelAndTokenizerLoader` 类来覆写对应的 `load_model` 和 `load_tokenizer` 函数，具体可以参照以下示例：
```python
class QwenModelAndTokenizerLoader(ModelAndTokenizerLoader):
    def __init__(self):
        super().__init__()
        pass
      
    def load_model(self, model_path: str):
        model = super().load_model(model_path)
        model.generation_config = GenerationConfig.from_pretrained(model_path)
        return model
    
    def load_tokenizer(self, model_path: str):
        tokenizer = super().load_tokenizer(model_path)
    
        # read generation config
        with open(model_path + '/generation_config.json', 'r') as f:
        generation_config = json.load(f)
        tokenizer.pad_token_id = generation_config['pad_token_id']
        tokenizer.eos_token_id = generation_config['eos_token_id']
        return tokenizer
```

#### 2. 编写 Model 的 context_builder 函数
如果输入需要转换为特定的格式（e.g. chatml 格式或者其他的 human-bot 格式），则需要去 `src.context_builder.context_builder_family` 中继承 ContextBuilder 类来覆写 make_context 函数，这个函数是用来将输入转换格式为对应需要的输出的，一个示例如下：
```python
class QwenChatContextBuilder(ContextBuilder):
    def __init__(self):
        super().__init__()
    
    def make_context(
        self,
        model,
        tokenizer, 
        query: str,
        system: str = "you are a helpful assistant"
    ):
      '''
  model: PretrainedModel
  tokenizer: PretrainedTokenzier
  query: Input string
  system: System prompt if needed
  '''
        im_start, im_end = "<|im_start|>", "<|im_end|>"
        im_start_tokens = [tokenizer.im_start_id]
        im_end_tokens = [tokenizer.im_end_id]
        nl_tokens = tokenizer.encode("\n")

        def _tokenize_str(role, content):
            return f"{role}\n{content}", tokenizer.encode(
                role, allowed_special=set()
            ) + nl_tokens + tokenizer.encode(content, allowed_special=set())

        system_text, system_tokens_part = _tokenize_str("system", system)
        system_tokens = im_start_tokens + system_tokens_part + im_end_tokens

        raw_text = ""
        context_tokens = []

        context_tokens = system_tokens + context_tokens
        raw_text = f"{im_start}{system_text}{im_end}" + raw_text
        context_tokens += (
            nl_tokens
            + im_start_tokens
            + _tokenize_str("user", query)[1]
            + im_end_tokens
            + nl_tokens
            + im_start_tokens
            + tokenizer.encode("assistant")
            + nl_tokens
        )
        raw_text += f"\n{im_start}user\n{query}{im_end}\n{im_start}assistant\n"
        return raw_text, context_tokens
```

#### 3. 注册模型到配置文件中
去 conf 中的 `model_conf.json`，注册对应的模型名和这个模型将要使用的 loader 和 context_builder，其中 loader 和 context_builder 写第一步和第二步中自定义的类名就可以，示例如下：
```json
{
  "Qwen-Chat": {
  "loader": "QwenModelAndTokenizerLoader",
  "context_builder": "QwenChatContextBuilder"
  }
}
```


#### 4. 执行测试脚本
直接运行以下代码发起测试
```Bash
# model_path: 要测试的模型路径
# model_name: 模型配置文件对应的模型命名，默认为 Default ，代表走默认的 loader 和 context_builder
# model_conf_path: 模型配置文件的地址，一般就为 conf 路径下的 devopseval_dataset_fp.json
# eval_dataset_list: 要测试的数据集名称，默认 all，全部测试，如果需要测试单个或者多个，用 # 符号链接，示例：dataset1#dataset2
# eval_dataset_fp_conf_path: 数据集配置地址
# eval_dataset_type: 测试哪种类型，只支持默认 test 类型的测试集
# data_path: 评测数据集地址，填写下载数据集后的地址就可以
# k_shot: 支持 0-5，代表 few-shot 会给模型前缀加的示例数量

  
python src/run_eval.py \
--model_path path_to_model \
--model_name model_name_in_conf \
--model_conf_path path_to_model_conf \
--eval_dataset_list all \
--eval_dataset_fp_conf_path path_to_dataset_conf \
--eval_dataset_type test \
--data_path path_to_downloaded_devops_eval_data \
--k_shot 0
```

举个🌰：比如评测数据集下载到了 `folder1`，代码放在了 `folder2`，模型在 `folder3`，模型不需要自定义 loader 和 context_builder，需要测试所有的数据集的 zero-shot 得分，那可以按照以下脚本发起测试：
```Bash
python folder2/src/run_eval.py \
--model_path folder3 \
--model_name Default \
--model_conf_path folder1/conf/model_conf.json \
--eval_dataset_list all \
--eval_dataset_fp_conf_path folder1/conf/devopseval_dataset_fp.json \
--eval_dataset_type test \
--data_path folder2 \
--k_shot 0
```
<br>