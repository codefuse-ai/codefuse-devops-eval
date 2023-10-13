# model_path: 要测试的模型路径
# model_name: 模型配置文件对应的模型命名
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
