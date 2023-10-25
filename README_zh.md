<p align="center"> <img src="images/devops_eval_logo.png" style="width: 100%;" id="title-icon">       </p>

<p align="center">
  🤗 <a href="https://huggingface.co/datasets/codefuse-admin/devopseval-exam" target="_blank">Hugging Face</a> • ⏬ <a href="#data" target="_blank">数据</a> • 📖 <a href="resources/tutorial.md" target="_blank">教程</a>
  <br>
  <a href="https://github.com/codefuse-ai/codefuse-devops-eval/blob/main/README.md"> English</a> | <a href="https://github.com/codefuse-ai/codefuse-devops-eval/blob/main/README_zh.md"> 中文 </a>
</p>

DevOps-Eval是一个专门为DevOps领域大模型设计的综合评估数据集。我们希望DevOps-Eval能够帮助开发者，尤其是DevOps领域的开发者，追踪进展并分析他们拥有的DevOps大模型的优势和不足之处。

📚 该仓库包含与DevOps和AIOps相关的问题和练习。

🔥️ 目前有 4850 个多项选择题，根据DevOps的通用流程将其归纳未8个模块，如[下图](images/data_info.png)所示。

💥 AIOps子类当前已有中英文样本2200例，覆盖的场景包括**日志解析**、**时序异常检测**、**时序分类**和**根因分析**。


<p align="center"> <a href="resources/devops_diagram_zh.jpg"> <img src="images/data_info.png" style="width: 100%;" id="data_info"></a></p>


## 🔔 更新
* **[2023.10.25]** 增加AIOps样本，包含日志解析、时序异常检测、时序分类和根因分析
* **[2023.10.18]** DevOps-Eval发布大模型评测排行版
<br>

## 📜 目录

- [🏆 排行榜](#-排行榜)
- [⏬ 数据](#-数据)
  - [👀 Notes](#-notes)
- [🚀 如何进行测试](#-如何进行测试)
- [🧭 TODO](#-todo)
- [🏁 Licenses](#-licenses)
- [😃 引用](#-引用)

## 🏆 排行榜
以下是我们获得的初版评测结果，包括多个开源模型的zero-shot和five-shot准确率。我们注意到，对于大多数指令模型来说，five-shot的准确率要优于zero-shot。

#### Zero Shot

| **模型**                 | plan  | code  | build | test  | release | deploy | operate | monitor |  **平均分**  |
|:------------------------:|:-----:|:-----:|:-----:|:------:|:--------:|:------:|:-------:|:--------:|:---------:|
| **DevOpsPal-14B-Chat** | 60.61 | 78.35 | 84.86 | 84.65 | 87.26 | 82.75 | 81.34 | 79.17 | **80.34** |
| **DevOpsPal-14B-Base** | 54.55 | 77.82 | 83.49 | 85.96 | 86.32 | 81.96 | 85.82 | 82.41 | **80.26** |
| Qwen-14B-Chat          |  60.61 | 75.4 | 85.32 | 84.21 | 89.62 | 82.75 | 83.58 | 80.56 |   79.28   |
| Qwen-14B-Base          |  57.58 | 73.81 | 84.4 | 85.53 | 86.32 | 81.18 | 82.09 | 80.09 |   77.92   |
| Baichuan2-13B-Base     |  60.61 | 69.42 | 79.82 | 79.82 | 82.55 | 81.18 | 85.07 | 83.8 |   75.10   |
| Baichuan2-13B-Chat     | 60.61 | 68.43 | 77.98 | 80.7 | 81.6 | 83.53 | 82.09 | 84.72 |   74.60   |
| **DevOpsPal-7B-Chat**  | 54.55 | 69.11 | 83.94 | 82.02 | 76.89 | 80 | 79.85 | 77.78 | **74.00** |
| **DevOpsPal-7B-Base**  | 54.55 | 68.96 | 82.11 | 78.95 | 80.66 | 76.47 | 79.85 | 78.7 | **73.55** |
| Qwen-7B-Base           | 53.03 | 68.13 | 78.9 | 75.44 | 80.19 | 80 | 83.58 | 80.09 |   73.13   |
| Qwen-7B-Chat           | 57.58 | 66.01 | 80.28 | 79.82 | 76.89 | 77.65 | 80.6 | 79.17 |   71.96   |
| Baichuan2-7B-Chat      |  54.55 | 63.66 | 77.98 | 76.32 | 71.7 | 73.33 | 75.37 | 79.63 |   68.17   |
| Internlm-7B-Chat       |  60.61 | 62.15 | 77.06 | 76.32 | 66.98 | 74.51 | 74.63 | 78.24 |   68.08   |
| Baichuan2-7B-Base      |  56.06 | 62.45 | 75.69 | 70.61 | 74.06 | 69.8 | 76.12 | 75.93 |   67.51   |
| Internlm-7B-Base       |  54.55 | 58.29 | 79.36 | 78.95 | 77.83 | 70.59 | 78.36 | 75.93 |   66.91   |


#### Five Shot

| **模型**                 | plan  | code  | build | test  | release | deploy | operate | monitor | **平均分**    |
|:------------------------:|:-----:|:-----:|:-----:|:------:|:--------:|:------:|:-------:|:--------:|:---------:|
| **DevOpsPal-14B-Chat** |63.64 | 79.49 | 81.65 | 85.96 | 86.79 | 86.67 | 89.55 | 81.48 | **81.77** |
| **DevOpsPal-14B-Base** |  62.12 | 80.55 | 82.57 | 85.53 | 85.85 | 84.71 | 85.07 | 80.09 | **81.70** |
| Qwen-14B-Chat |  65.15 | 76 | 82.57 | 85.53 | 84.91 | 84.31 | 85.82 | 81.48 | 79.55 |
| Qwen-14B-Base |  66.67 | 76.15 | 84.4 | 85.53 | 86.32 | 80.39 | 86.57 | 80.56 | 79.51 |
| Baichuan2-13B-Base | 63.64 | 71.39 | 80.73 | 82.46 | 81.13 | 84.31 | 91.79 | 85.19 | 77.09 |
| Qwen-7B-Base | 75.76 | 72.52 | 78.9 | 81.14 | 83.96 | 81.18 | 85.07 | 81.94 | 77.02 |
| Baichuan2-13B-Chat | 62.12 | 69.95 | 76.61 | 84.21 | 83.49 | 79.61 | 88.06 | 80.56 | 75.32 |
| **DevOpsPal-7B-Chat** | 66.67 | 69.95 | 83.94 | 81.14 | 80.19 | 82.75 | 82.84 | 76.85 | **75.25** |
| **DevOpsPal-7B-Base** |  69.7 | 69.49 | 82.11 | 81.14 | 82.55 | 82.35 | 80.6 | 79.17 | **75.17** |
| Qwen-7B-Chat |  65.15 | 66.54 | 82.57 | 81.58 | 81.6 | 81.18 | 80.6 | 81.02 | 73.62 |
| Baichuan2-7B-Base | 60.61 | 67.22 | 76.61 | 75 | 77.83 | 78.43 | 80.6 | 79.63 | 72.11 |
| Internlm-7B-Chat |  60.61 | 63.06 | 79.82 | 80.26 | 67.92 | 75.69 | 73.88 | 77.31 | 71.09 |
| Baichuan2-7B-Chat |  60.61 | 64.95 | 81.19 | 75.88 | 71.23 | 75.69 | 78.36 | 79.17 | 70.49 |
| Internlm-7B-Base |  62.12 | 65.25 | 77.52 | 80.7 | 74.06 | 78.82 | 79.85 | 75.46 | 69.17 |

## ⏬ 数据
#### 下载
* 方法一：下载zip压缩文件（你也可以直接用浏览器打开下面的链接）：
  ```
  wget https://huggingface.co/datasets/codefuse-admin/devopseval-exam/resolve/main/devopseval-exam.zip
  ```
  然后可以使用 pandas加载数据：

  ```
  import os
  import pandas as pd
  
  File_Dir="devopseval-exam"
  test_df=pd.read_csv(os.path.join(File_Dir,"test","UnitTesting.csv"))
  ```
* 方法二：使用[Hugging Face datasets](https://huggingface.co/datasets/codefuse-admin/devopseval-exam)直接加载数据集。示例如下：
  ```python
  from datasets import load_dataset
  dataset=load_dataset(r"DevOps-Eval/devopseval-exam",name="UnitTesting")
  
  print(dataset['val'][0])
  # {"id": 1, "question": "单元测试应该覆盖以下哪些方面？", "A": "正常路径", "B": "异常路径", "C": "边界值条件"，"D": 所有以上，"answer": "D", "explanation": ""}  ```
#### 👀 说明
为了方便使用，我们已经整理出了 53 个细分类别以及它们的中英文名称。具体细节请查看 [category_mapping.json](resources/categroy_mapping.json) 。格式如下：

```
{
  "UnitTesting.csv": [
    "unit testing",
    "单元测试",
    {"dev": 5, "test": 32}
    "TEST"
  ],
  ...
  "file_name":[
  "英文名称",
  "中文名称",
  "样本数量",
  "类别(PLAN,CODE,BUILD,TEST,RELEASE,DEPOLY,OPERATE,MONITOR八选一)"
  ]
}
```
每个细分类别由两个部分组成：dev 和 test。每个细分类别的 dev 集包含五个示范实例以及为 few-shot 评估提供的解释。而 test 集则用于模型评估，并且test数据已包含准确标签。

下面是 dev 数据的示例，来自"版本控制"细分类别：
```
id: 4
question: 如何找到Git特定提交中已更改的文件列表？
A: 使用命令 `git diff --name-only SHA`
B: 使用命令 `git log --name-only SHA`
C: 使用命令 `git commit --name-only SHA`
D: 使用命令 `git clone --name-only SHA`
answer: A
explanation: 
分析原因：
git diff --name-only SHA命令会显示与SHA参数对应的提交中已修改的文件列表。参数--name-only让命令只输出文件名，而忽略其他信息。其它选项中的命令并不能实现此功能。
```

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

## 🧭 TODO
- [x] 添加AIOps样本
- [ ] 添加AIOps场景，比如**时间预测**
- [ ] 当前各类别样本量不平均，后续进一步增加样本数量
- [ ] 增加困难程度的样本集
- [ ] 增加样本的英文版本

<br>
<br>

## 🏁 Licenses
<br>

## 😃 引用

如果您使用了我们的数据集，请引用我们的论文。
<br>
<br>
