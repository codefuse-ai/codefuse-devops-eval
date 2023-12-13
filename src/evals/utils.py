
def rec_search_key(res, k="", skeys: list=[], s=""):
    '''递归进行分析是否存在key被获取'''
    if isinstance(res, dict):
        for new_k, v in res.items():
            try:
                skeys = rec_search_key(v, ".".join([str(k), str(new_k)]) if k else new_k, skeys, s)
            except Exception as e:
                print(res, k, new_k)
                raise e
    elif isinstance(res, list):
        for i in res:
            skeys = rec_search_key(i, k + ".list", skeys, s)
    else:
        if str(res) in str(s):
            skeys.append(k[:-5] if k[-5:] == ".list" else k)
            return list(set(skeys))
    return list(set(skeys))


    