# -*- coding: utf-8 -*-
from google.appengine.ext import db

def getNextNum():
    def procedure():
        num = MAXNUM.get_by_key_name('URL')
        if num is None:
            num = MAXNUM(key_name = 'URL')
        
        num.max_num = num.max_num + 1
        num.put()
        return num.max_num
    return db.run_in_transaction(procedure)

class MAXNUM(db.Model):
    max_num = db.IntegerProperty(default = 0)