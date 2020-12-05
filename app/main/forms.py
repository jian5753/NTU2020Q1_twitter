# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:39:20 2020

@author: ZuroChang
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField
from wtforms.fields.core import IntegerField, SelectFieldBase
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

class NewTopicForm(FlaskForm):
    topicName = StringField('new topic name')
    submit = SubmitField('add new topic')
    
class EditTopicForm(FlaskForm):
    topicToEdit = SelectField('select a topic')
    newKeyWord = StringField('new key words')
    keyWordWeight = StringField('weights')
    submit = SubmitField('add new topic')
    
class DeleteTopicForm(FlaskForm):
    topicToDel = SelectMultipleField('select topics')
    submit = SubmitField('delete')

class SelectOneTopic(FlaskForm):
    theTopic = SelectField('select a topic')
    submit = SubmitField('select')