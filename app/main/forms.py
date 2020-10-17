# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:39:20 2020

@author: ZuroChang
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    dataLocation=StringField('ennter the directory', validators=[DataRequired()])
    submit=SubmitField('submit')

