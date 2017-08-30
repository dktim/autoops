#coding=utf-8

'''
正则表达式工具

@author: Huiyugeng
'''

import re

'''
正则表达式解析字符串

@param regex: 正则表达式
@param line: 需要解析的字符串

@return: 解析的结果 
'''
def get_line(regex , line):
    items = []
    
    pattern = re.compile(regex)
    match = pattern.match(line)
    if match:
        items = match.groups()
                
    return items

'''
判断字符串是否与正则表达式匹配

@param regex: 正则表达式
@param line: 需要匹配的字符串

@return: 匹配的结果，True 匹配 False 不匹配
'''    
def check_line(regex, line):
    pattern = re.compile(regex)
    match = pattern.match(line)
    if match:
        return True
    else:
        return False
    
'''
根据指定正则表达式匹配的结果进行替换

@param regex: 正则表达式
@param repl: 替换的内容
@param line: 需要匹配的字符串
@param count: 匹配替换的个数,0表示任意个数

@return: 匹配替换后的结果
'''
def sub(regex, repl, line, count=0):
    return re.sub(regex, repl, line, count)

'''
根据指定正则表达式匹配的结果进行分割字符串

@param regex: 正则表达式
@param line: 分割的内容

@return: 分割后的结果，list类型
'''
def split(regex, line):
    return re.split(regex, line)
