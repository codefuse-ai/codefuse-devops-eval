
TOOL_FILL_BASE_PROMPT = '''你现在是一位参数填充助手，帮助我从历史问题问答中抽取出指定API入参结构所需要的参数信息
HISTORY_QUESTION: {query}
API_SCHEMA: {api_schema}
返回json结构的API调用参数:
'''


TOOL_PARSER_BASE_PROMPT = '''你现在是一位API调用解析，帮助我生成可解析API_RESPONSE来回答用户问题的代码
HISTORY_QUESTION: {query}
API_SCHEMA: {api_schema}
API_RESPONSE: {response}
返回解析response的代码:
'''

TOOL_SUMMARY_BASE_PROMPT = '''你现在是一位API调用总结助手，帮助我从API的RESPONSE中获取到特定的信息，来回答用户问题
HISTORY_QUESTION: {query}
API_SCHEMA: {api_schema}
API_RESPONSE: {response}
返回回答结果:
'''
