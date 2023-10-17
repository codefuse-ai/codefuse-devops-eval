<p align="center"> <img src="images/DevOps-Eval Logo.png" style="width: 50%;" id="title-icon">       </p>

# <p align="center">A DevOps Domain Knowledge Evaluation Benchmark for Large Language Models</p>

<p align="center">
  🤗 <a href="https://huggingface.co/datasets/DevOps-Eval/devopseval-exam" target="_blank">Hugging Face</a> • ⏬ <a href="#data" target="_blank">Data</a> • 📖 <a href="resources/tutorial.md" target="_blank">Tutorial (ZH)</a>
  <br>
  <a href="https://github.com/codefuse-ai/codefuse-devops-eval/blob/main/README_zh.md">   中文</a> | <a href="https://github.com/codefuse-ai/codefuse-devops-eval/blob/main/README.md"> English </a>
</p>

DevOps-Eval is a comprehensive evaluation suite specifically designed for foundation models in the DevOps field. It consists of xxxx multi-choice questions spanning 8 diverse disciplines, as shown below.

We hope DevOps-Eval could help developers, especially in the DevOps field, track the progress and analyze the important strengths/shortcomings of their models.



:pencil: &nbsp;This repo contains questions and exercises related to DevOps and AIOps

:bar_chart: &nbsp;There are currently **2650** exercises and questions

<center>
<table style="width: 100%; height: 100%;">
  <tr>
    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
            <img src="images/icon/jama.png"  width="50px;" height="50px;" alt="PLAN" />
    <br /><span style="font-size: 8px;">REQM</span></a></td>
    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
            <img src="images/icon/pivotal-tracker.png"  width="50px;" height="50px;" alt="PLAN" />
    <br /><span style="font-size: 8px;">ProgM</span></a></td>
    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
            <img src="images/icon/design.png"  width="50px;" height="50px;" alt="PLAN" /> 
    <br /><span style="font-size: 8px;">Design</span></a></td>
    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
            <img src="images/icon/spark.png"  width="50px;" height="50px;" alt="PLAN" />
    <br /><span style="font-size: 8px;">Frameworks</span></a></td>
    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
        <img src="images/icon/git.png"  width="50px;" height="50px;" alt="PLAN" /> 
    <br /><span style="font-size: 8px;">SCM/VCS</span></a></td>
    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
            <img src="images/icon/packer.png"  width="50px;" height="50px;" alt="PLAN" />
    <br /><span style="font-size: 8px;">PackageMgnt</span></a></td>
    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
            <img src="images/icon/Junit.png"  width="50px;" height="50px;" alt="PLAN" />
    <br /><span style="font-size: 8px;">UnitTesting</span></a></td>
    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
            <img src="images/icon/selenium.png"  width="50px;" height="50px;" alt="PLAN" />
    <br /><span style="font-size: 8px;">IntTesting</span></a></td>

  </tr>
  <tr>
    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
            <img src="images/icon/risk.png"  width="50px;" height="50px;" alt="PLAN" />
    <br /><span style="font-size: 8px;">RiskMgnt</span></a></td>
    <td align="center"> </td>
    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
        <img src="images/icon/programming.png"  width="50px;" height="50px;" alt="PLAN" /> 
    <br /><span style="font-size: 8px;">General</span></a></td>
    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
        <img src="images/icon/python.png"  width="50px;" height="50px;" alt="PLAN" /> 
    <br /><span style="font-size: 8px;">Prog</span></a></td>
    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
            <img src="images/icon/databases.png"  width="50px;" height="50px;" alt="PLAN" />
    <br /><span style="font-size: 8px;">DBMgmt</span></a></td>
    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
            <img src="images/icon/maven.png"  width="50px;" height="50px;" alt="PLAN" />
    <br /><span style="font-size: 8px;">DepMgmt</span></a></td>
    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
            <img src="images/icon/system_testing.png"  width="50px;" height="50px;" alt="PLAN" />
    <br /><span style="font-size: 8px;">SystemTesting</span></a></td>
    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
                <img src="images/icon/uat.png"  width="50px;" height="50px;" alt="PLAN" />
    <br /><span style="font-size: 8px;">UAT</span></a></td>
  </tr>
  <tr>
    <td align="center"> </td>
    <td align="center"> </td>
    <td align="center"> </td>
    <td align="center"> </td>
    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
            <img src="images/icon/vscode.png"  width="50px;" height="50px;" alt="PLAN" />
    <br /><span style="font-size: 8px;">Compile</span></a></td>
    <td align="center"> </td>
    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
            <img src="images/icon/jmeter.svg"  width="50px;" height="50px;" alt="PLAN" />
    <br /><span style="font-size: 8px;">PT</span></a></td>
    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
            <img src="images/icon/security.png"  width="50px;" height="50px;" alt="PLAN" />
    <br /><span style="font-size: 8px;">SecurityTesting</span></a></td>
  </tr>
  <tr>
    <td colspan="2" align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
    <b><span style="font-size: 10px;">PLAN</span></b></a></td>
    <td colspan="2" align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
    <b><span style="font-size: 10px;">CODE</span></b></a></td>
    <td colspan="2" align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
    <b><span style="font-size: 10px;">BUILD</span></b></a></td>
    <td colspan="2" align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">
    <b><span style="font-size: 10px;">TEST</span></b></a></td>
  </tr>

[//]: # (  <tr>)

[//]: # (    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">)

[//]: # (            <img src="images/icon/Junit.png"  width="50px;" height="50px;" alt="PLAN" />)

[//]: # (    <br />UnitTesting</a></td>)

[//]: # (    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">)

[//]: # (            <img src="images/icon/selenium.png"  width="50px;" height="50px;" alt="PLAN" />)

[//]: # (    <br />IntegrationTesting</a></td>)

[//]: # (    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">)

[//]: # (            <img src="images/icon/cicd.png"  width="50px;" height="50px;" alt="PLAN" />)

[//]: # (    <br />CI/CD</a></td>)

[//]: # (    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">)

[//]: # (            <img src="images/icon/docker.png"  width="50px;" height="50px;" alt="PLAN" />)

[//]: # (    <br />ArtifactsMgmt</a></td>)

[//]: # (    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">)

[//]: # (            <img src="images/icon/ansible.png"  width="50px;" height="50px;" alt="PLAN" />)

[//]: # (    <br />ConfigMgmt</a></td>)

[//]: # (    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">)

[//]: # (            <img src="images/icon/terraform.png"  width="50px;" height="50px;" alt="PLAN" />)

[//]: # (    <br />Provisioning</a></td>)

[//]: # (  </tr>)

[//]: # (  <tr>)

[//]: # (    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">)

[//]: # (            <img src="images/icon/system_testing.png"  width="50px;" height="50px;" alt="PLAN" />)

[//]: # (    <br />SystemTesting</a></td>)

[//]: # (    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">)

[//]: # (                <img src="images/icon/uat.png"  width="50px;" height="50px;" alt="PLAN" />)

[//]: # (    <br />UAT</a></td>)

[//]: # (<td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">)

[//]: # (            <img src="images/icon/linux.png"  width="50px;" height="50px;" alt="PLAN" />)

[//]: # (    <br />Linux</a></td>)

[//]: # (    <td align="center"> </td>)

[//]: # (    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">)

[//]: # (            <img src="images/icon/cloud.png"  width="50px;" height="50px;" alt="PLAN" />)

[//]: # (    <br />Cloud</a></td>)

[//]: # (    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">)

[//]: # (            <img src="images/icon/infrastructure_as_code.svg"  width="50px;" height="50px;" alt="PLAN" />)

[//]: # (    <br />IAC</a></td>)

[//]: # (  </tr>)

[//]: # (  <tr>)

[//]: # (    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">)

[//]: # (            <img src="images/icon/jmeter.svg"  width="50px;" height="50px;" alt="PLAN" />)

[//]: # (    <br />PT</a></td>)

[//]: # (    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">)

[//]: # (            <img src="images/icon/security.png"  width="50px;" height="50px;" alt="PLAN" />)

[//]: # (    <br />SecurityTesting</a></td>)

[//]: # (    <td align="center"> </td>)

[//]: # (    <td align="center"> </td>)

[//]: # (    <td align="center"> </td>)

[//]: # (    <td align="center"> </td>)

[//]: # ()
[//]: # (  </tr>)

[//]: # (  <tr>)

[//]: # (    <td colspan="2" align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 85%;">)

[//]: # (    <b>TEST</b></a></td>)

[//]: # (    <td colspan="2" align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 85%;">)

[//]: # (    <b>RELEASE</b></a></td>)

[//]: # (    <td colspan="2" align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 85%;">)

[//]: # (    <b>DEPLOY</b></a></td>)

[//]: # (  </tr>)

[//]: # ()
[//]: # (  <tr>)

[//]: # (    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">)

[//]: # (            <img src="images/icon/kubernetes.png"  width="50px;" height="50px;" alt="PLAN" />)

[//]: # (    <br />Containerization</a></td>)

[//]: # (    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">)

[//]: # (            <img src="images/icon/virtualization.png"  width="50px;" height="50px;" alt="PLAN" />)

[//]: # (    <br />Virtualization</a></td>)

[//]: # (    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">)

[//]: # (            <img src="images/icon/logging.png"  width="50px;" height="50px;" alt="PLAN" />)

[//]: # (    <br />Data</a></td>)

[//]: # (    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">)

[//]: # (                <img src="images/icon/prometheus.png"  width="50px;" height="50px;" alt="PLAN" />)

[//]: # (    <br />Alert</a></td>)

[//]: # (    <td align="center"> </td>)

[//]: # (    <td align="center"> </td>)

[//]: # (  </tr>)

[//]: # (  <tr>)

[//]: # (    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">)

[//]: # (            <img src="images/icon/chaos_engineering.png"  width="50px;" height="50px;" alt="PLAN" />)

[//]: # (    <br />OperateSecne</a></td>)

[//]: # (    <td align="center"> </td>)

[//]: # (    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">)

[//]: # (            <img src="images/icon/grafana.png"  width="50px;" height="50px;" alt="PLAN" />)

[//]: # (    <br />Visualization</a></td>)

[//]: # (    <td align="center"><a src="images/devops_diagram_zh.jpg" style="zoom: 100%;">)

[//]: # (            <img src="images/icon/observability.png"  width="50px;" height="50px;" alt="PLAN" />)

[//]: # (    <br />Analysis</a></td>)

[//]: # (    <td align="center"> </td>)

[//]: # (    <td align="center"> </td>)

[//]: # (  </tr>)

[//]: # (  <tr>)

[//]: # (    <td colspan="2" align="center" height="10px"><a src="images/devops_diagram_zh.jpg" style="zoom: 85%;">)

[//]: # (    <b>OPERATE</b></a></td>)

[//]: # (    <td colspan="2" align="center" height="10px;"><a src="images/devops_diagram_zh.jpg" style="zoom: 85%;">)

[//]: # (    <b>MONITOR</b></a></td>)

[//]: # (    <td colspan="2" align="center" height="10px;"><b></b></td>)

[//]: # (  </tr>)
</table>
</center>


    
## News

* **[2023.09.30]** DevOps-Eval...
<br>
<br>

## Table of Contents

- [Leaderboard](#leaderboard)
- [Results On Validation Split](#results-on-validation-split)
- [Data](#data)
- [How to Evaluate](#how-to-evaluate)
- [TODO](#todo)
- [Licenses](#licenses)
- [Citation](#citation)

## Leaderboard
coming soon
<br>
<br>

## Results On Validation Split
coming soon
<br>
<br>

## Data
#### Download
* Method 1: Download the zip file (you can also simply open the following link with the browser):
  ```
  wget https://huggingface.co/datasets/DevOps-Eval/devopseval-exam/resolve/main/data.zip
  ```
  then unzip it and you may load the data with pandas:
  ```
  import os
  import pandas as pd
  
  File_Dir="devopseval-exam"
  test_df=pd.read_csv(os.path.join(File_Dir,"test","UnitTesting.csv"))
  ```
* Method 2: Directly load the dataset using [Hugging Face datasets](https://huggingface.co/datasets/DevOps-Eval/devopseval-exam):
  ```python
  from datasets import load_dataset
  dataset=load_dataset(r"DevOps-Eval/devopseval-exam",name="UnitTesting")
  
  print(dataset['val'][0])
  # {"id": 1, "question": "单元测试应该覆盖以下哪些方面？", "A": "正常路径", "B": "异常路径", "C": "边界值条件"，"D": 所有以上，"answer": "D", "explanation": ""}  ```
#### Notes
To facilitate usage, we have organized the category name handlers and English/Chinese names corresponding to 49 categories. Please refer to [category_mapping.json](https://github.com/codefuse-ai/codefuse-devops-eval/category_mapping.json) for details. The format is:

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
  "English Name",
  "Chinese Name",
  "Sample Number",
  "Supercatagory Label(PLAN,CODE,BUILD,TEST,RELEASE,DEPOLY,OPERATE,MONITOR choose 1 out of 8)"
  ]
}
```
Each subject consists of two splits: dev and test.  The dev set per subject consists of five exemplars with explanations for few-shot evaluation. And the test set is for model evaluation. Labels on the test split are also released.

Below is a dev example from 'version control':

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

## How to Evaluate
If you need to test your own huggingface-formatted model, the overall steps are as follows:
1. Write the loader function for the model.
2. Write the context_builder function for the model.
3. Register the model in the configuration file.
4. Run the testing script.
If the model does not require any special processing after loading, and the input does not need to be converted to a specific format (e.g. chatml format or other human-bot formats), you can directly proceed to step 4 to initiate the testing.

#### 1. Write the loader function
If the model requires additional processing after loading (e.g. adjusting the tokenizer), you need to inherit the `ModelAndTokenizerLoader` class in `src.context_builder.context_builder_family.py` and override the corresponding `load_model` and `load_tokenizer` functions. You can refer to the following example:
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

#### 2. Write the context_builder function for the Model
If the input needs to be converted to a specific format (e.g. chatml format or other human-bot formats), you need to inherit the ContextBuilder class in `src.context_builder.context_builder_family` and override the make_context function. This function is used to convert the input to the corresponding required format. An example is shown below:
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

#### 3. Register the model in the configuration file
Go to the `model_conf.json` file in the conf directory and register the corresponding model name and the loader and context_builder that will be used for this model. Simply write the class names defined in the first and second steps for the loader and context_builder. Here is an example:
```json
{
  "Qwen-Chat": {
  "loader": "QwenModelAndTokenizerLoader",
  "context_builder": "QwenChatContextBuilder"
  }
}
```

#### 4. Execute the testing script
Run the following code to initiate the test:
```Bash
# model_path: path to the model for testing
# model_name: the model name corresponding to the model in the configuration file, default is Default, which represents using the default loader and context_builder
# model_conf_path: path to the model configuration file, usually the devopseval_dataset_fp.json file in the conf directory
# eval_dataset_list: the names of the datasets to be tested, default is all to test all datasets, if you need to test one or more datasets, use the # symbol to connect them, for example: dataset1#dataset2
# eval_dataset_fp_conf_path: path to the dataset configuration file
# eval_dataset_type: the type of testing, only supports the default test type of test dataset
# data_path: path to the evaluation dataset, fill in the downloaded dataset address
# k_shot: supports 0-5, represents the number of example prefixes added for few-shot

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

For example, if the evaluation dataset is downloaded to `folder1`, the code is placed in `folder2`, and the model is in `folder3`, and the model does not require custom loader and context_builder, and all zero-shot scores of all datasets need to be tested, you can use the following script to initiate the test:
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

## TODO
<br>
<br>


## Citation

Please cite our paper if you use our dataset.
<br>
<br>
