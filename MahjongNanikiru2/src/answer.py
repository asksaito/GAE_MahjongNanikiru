# -*- coding: utf-8 -*-
from google.appengine.ext import db

class Answer(db.Model):
    question_no = db.IntegerProperty(required=True)
    pai = db.IntegerProperty(required=True)
    vote_num = db.IntegerProperty(default=0)
    
#    def __init__(self):
#        self.question_no = question_no
#        self.pai = in_pai
#        self.vote_num = 0
        