import json
import jsonlines
import os
import pandas as pd

from loguru import logger

from src.hparams.evaluate_args import EvaluateArguments
from src.data.data_preprocess import preprocess


def load_all_dataset(eval_args: EvaluateArguments):
    '''
    Load all eval dataset
    '''
    # get fp for eval dataset
    dataset_name_list = eval_args.eval_dataset_list
    eval_dataset_fp_conf_path = eval_args.eval_dataset_fp_conf_path

    with open(eval_dataset_fp_conf_path, 'r') as f:
        dataset_fn_dict = json.load(f)

    data_dir = eval_args.data_path

    logger.info(dataset_name_list)
    if len(dataset_name_list) == 1 and dataset_name_list[0] == 'all':
        dataset_name_list = dataset_fn_dict.keys()
        dataset_fp_list = [data_dir + os.path.sep + eval_args.eval_language + os.path.sep + eval_args.eval_dataset_type + os.path.sep + dataset_fn_dict[i] for i in dataset_name_list]

    logger.info('Start load and preprocess dataset')
    all_dataset = {}
    for dataset_name in dataset_name_list:
        dataset_fp = data_dir + os.path.sep + eval_args.eval_language + os.path.sep + eval_args.eval_dataset_type + os.path.sep + dataset_fn_dict[dataset_name]
        df = pd.read_csv(dataset_fp)

        # Read dev data if doing few-shot test
        df_dev = None
        if eval_args.k_shot > 0:
            dev_dataset_fp = data_dir + os.path.sep + eval_args.eval_language + os.path.sep + 'dev' + os.path.sep + dataset_fn_dict[dataset_name]
            df_dev = pd.read_csv(dev_dataset_fp)

        all_dataset[dataset_name] = preprocess(df, eval_args, df_dev=df_dev)
        logger.info('Load success, dataset_name={}, dataset_file_path={}, dataset question count={}'.format(dataset_name, 
                                                                                                            dataset_fp, 
                                                                                                            len(all_dataset[dataset_name])))
    return all_dataset
    
if __name__ == '__main__':
    a = os.path.split(os.path.realpath(__file__))[0]
    b = os.path.abspath(os.path.dirname(a)+os.path.sep+"../data")
    logger.debug(b)
