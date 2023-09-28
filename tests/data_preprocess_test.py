import sys
sys.path.append('/mnt/llm/DevOpsEval')
from src.data.data_preprocess import preprocess_zero_shot

import pandas as pd
from loguru import logger


if __name__ == '__main__':
    df = pd.read_csv('/mnt/llm/DevOpsEval/data/devopseval/dev/integration.csv')
    d = preprocess_zero_shot(df)
    logger.info(d[0]['query'])
