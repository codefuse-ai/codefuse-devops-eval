def get_acc_score(all_pred):
    '''
    Get accuracy score by dataset
    '''
    score_dict = {i:None for i in all_pred}
    total_corr = 0
    total_count = 0
    for dataset_name, dataset_pred in all_pred.items():
        corr = 0

        for pred_single in dataset_pred:
            if pred_single['answer'] == pred_single['pred']:
                corr += 1
        score_dict[dataset_name] = {
            'total': len(dataset_pred),
            'corr': corr,
            'score': corr / len(dataset_pred)
        }

        total_corr += corr
        total_count += len(dataset_pred)
    res = {
        'total': total_count,
        'corr': total_corr,
        'score': total_corr / total_count,
        'detail': score_dict
    }
    return res
