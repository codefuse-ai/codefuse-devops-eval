import pandas as pd
from loguru import logger


def preprocess(df: pd.DataFrame, eval_args, df_dev: pd.DataFrame = None):
    '''
    Preprocess df and generate final dict
    '''
    question_prompt = '''以下是关于开发运维领域的单项选择题，请选出其中的正确答案。请直接输出选项。\n'''

    if eval_args.k_shot > 0 and df_dev is not None:
        # uppercase to lowercase
        df_dev.rename(columns={
            'Question': 'question',
            'Answer': 'answer'
        }, inplace=True)

        prefix = ''

        for idx in range(eval_args.k_shot):
            question = df_dev['question'].iloc[idx]
            prefix = prefix + question_prompt + '问题：' + question + '\n'

            for option in ['A', 'B', 'C', 'D']:
                if df_dev[option].iloc[idx]:
                    prefix += '{}. {}\n'.format(option, df_dev[option].iloc[idx])
            prefix += '答案：{}\n'.format(df_dev['answer'].iloc[idx].strip().upper())
        prefix = prefix + question_prompt
        res = preprocess_question(df, prefix)
    else:
        res = preprocess_question(df, question_prompt)
    
    return res

def preprocess_question(df: pd.DataFrame, prefix: str = ''):
    '''
    Preprocess df and generate final dict
    '''
    res = []

    # uppercase to lowercase
    df.rename(columns={
        'Question': 'question',
        'Answer': 'answer'
    }, inplace=True)

    for idx in range(df.shape[0]):
        to_append = {
            'question': df['question'].iloc[idx],
            'options': [],
            'answer': df['answer'].iloc[idx].strip().upper()
        }
        question = df['question'].iloc[idx]

        query = prefix + '''问题：{question}\n'''.format(question=question)

        for option in ['A', 'B', 'C', 'D']:
            if df[option].iloc[idx]:
                to_append['options'].append(option)
                to_append[option] = df[option].iloc[idx]
                to_add = '{}. {}\n'.format(option, df[option].iloc[idx])
                query += to_add
        
        to_add = '答案：'
        query += to_add
        to_append['query'] = query
        res.append(to_append)
    return res
