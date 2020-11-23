# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:39:20 2020

@author: ZuroChang
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import IntegerField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    dataLocation=StringField('enter the directory', validators=[DataRequired()])
    submit=SubmitField('submit')

class KeyWordForm(FlaskForm):
    searchKey = StringField('enter keywords')
    submit=SubmitField('search')

class wordStatForm(FlaskForm):
    searchAuthor = StringField('search author')
    rankRange = IntegerField('rank range')
    submit = SubmitField('search')

