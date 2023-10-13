import torch
import copy

from loguru import logger


def evaluate(model, tokenizer, context_builder, all_dataset):
    '''
    Evaluate on all_dataset
    '''
    all_dataset_pred = copy.deepcopy(all_dataset)

    do_verbose = True
    for dataset_name, dataset in all_dataset_pred.items():
        for question in dataset:
            if do_verbose:
                question['pred'] = get_pred(model, tokenizer, context_builder, question, do_verbose)
                do_verbose = False
            else:
                question['pred'] = get_pred(model, tokenizer, context_builder, question, do_verbose)
    return all_dataset_pred

def get_pred(model, tokenizer, context_builder, question: dict, verbose: bool = False):
    '''
    Get the prediction for single question
    '''
    options = question['options']
    query = question['query']

    option_dict = {}
    for option in options:
        encoded = tokenizer.encode(option)

        if len(encoded) == 1:
            option_dict[option] = encoded
        else:
            option_dict[option] = tokenizer._convert_token_to_id(option)

    # build context
    raw_text, context_tokens = context_builder.make_context(model, tokenizer, query)
    input_ids = torch.tensor([context_tokens]).to(model.device)

    if verbose:
        logger.info('sample raw_text={}\ncontext_tokens={}\nlen of context_tokens={}'.format(raw_text, context_tokens, len(context_tokens)))
    
    # if len(context_tokens) > 900:
    #     return 'A'

    # feed to the model
    output = model(input_ids)
    logits = output.logits

    # get pred option
    score_dict = {}
    for option in option_dict:
        score = logits[0][-1][option_dict[option]]
        score_dict[option] = float(score)
    # logger.debug('score_dict={}'.format(score_dict))

    max_score = float('-inf')
    best_option = None
    for option, score in score_dict.items():
        if score > max_score:
            max_score = score
            best_option = option
    if verbose:
        logger.debug('score_dict={}, max_score={}, best_option={}, answer={}'.format(score_dict, max_score, best_option, question['answer']))
    return best_option

