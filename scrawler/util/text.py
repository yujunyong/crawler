# -*- coding: utf-8 -*-

def strip(text):
    """
        去除首尾多余的字符( \r\n\t)
    """
    if type(text) == list:
        return [item.strip(' \r\n\t') for item in text]
    else:
        return text.strip(' \r\n\t')
