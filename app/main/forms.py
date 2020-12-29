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
    submit = SubmitField('save change')
    
class DeleteTopicForm(FlaskForm):
    topicToDel = SelectMultipleField('select topics')
    submit = SubmitField('delete')

class SelectOneTopic(FlaskForm):
    theTopic = SelectField('select a topic')
    submit = SubmitField('select')

class AddStopWord(FlaskForm):
    stopWord = StringField('add stop words')
    submit = SubmitField('add')

class AddStopRule(FlaskForm):
    stopRuleType = SelectField(
        'select a type',
        choices= ['length lower bound', 'length upper bound', 'regex']
    )
    stopRule_bound = IntegerField('bound')
    stopRule_regex = StringField('regex')
    submit = SubmitField('add')