# -*- coding: utf-8 -*-
import logging

from django.utils import simplejson

class ResponseFormatJSON(object):
    '''
    Response Creator
    '''
    def __init__(self):
        '''
        Constructor
        '''
    
    def create(self, api_name, result, data = {}, errcode = 0, errmsg = ''):
        # レスポンス作成
        response = simplejson.loads(simplejson.dumps({"API":api_name, "Result":result, "Data":{}, "ErrCode":errcode, "ErrMsg":errmsg}, ensure_ascii=False,sort_keys=True))
        # データ部
        for key in data:
            response['Data'][key] = data[key]        
        
        # JSON形式の文字列で返す
        str = simplejson.dumps(response,ensure_ascii=False,sort_keys=True)
        logging.debug(str)
        return str

