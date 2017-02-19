# -*- coding: utf-8 -*-
from google.appengine.ext import db

class Question(db.Model):
	#no = db.IntegerProperty()
	author = db.StringProperty()
	title = db.StringProperty()
	detail = db.StringProperty()
	bakyo = db.IntegerProperty()
	honba = db.IntegerProperty()
	cha = db.IntegerProperty()
	junme = db.IntegerProperty()
	tenbo = db.IntegerProperty()
	tehai = db.ListProperty(int)
	#tehai = db.StringProperty()
	tsumo = db.IntegerProperty()
	#dora = db.IntegerProperty()
	dora = db.ListProperty(int)
	date = db.DateTimeProperty(auto_now_add=True)
