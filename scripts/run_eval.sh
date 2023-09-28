set -v

cd /mnt/llm/DevOpsEval

# python src/run_eval.py \
#     --model_path /mnt/llm/devopspal/model/Qwen-7B \
#     --model_name Qwen-7b-Base \
#     --model_conf_path /mnt/llm/DevOpsEval/conf/model_conf.json \
#     --eval_dataset_list college_programming#computer_architecture#computer_network \
#     --eval_dataset_fp_conf_path /mnt/llm/DevOpsEval/conf/dataset_fp.json \
#     --eval_dataset_type val \
#     --k_shot 0

python src/run_eval.py \
    --model_path /mnt/llm/devopspal/model/trained/devopspal-sft-7b-v1.4/checkpoint-1563 \
    --model_name Qwen-7b-Chat \
    --model_conf_path /mnt/llm/DevOpsEval/conf/model_conf.json \
    --eval_dataset_list risk_csv \
    --eval_dataset_fp_conf_path /mnt/llm/DevOpsEval/conf/dataset_fp.json \
    --eval_dataset_type val \
    --data_path /mnt/llm/DevOpsEval/data/devopseval \
    --k_shot 0
