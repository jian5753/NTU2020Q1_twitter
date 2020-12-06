# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:08:41 2020

@author: ZuroChang
"""


from flask import Flask #,render_template
from flask_bootstrap import Bootstrap
# from flask_mail import Mail
# from flask_moment import Moment
# from flask_sqlalchemy import SQLAlchemy
from config import config
import os
from pathlib import Path

bootstrap=Bootstrap()
# mail=Mail()
# moment=Moment()
# db=SQLAlchemy()

def create_app(config_name='default'):
    app=Flask(__name__)
    
    app.config.from_object(config[config_name])
    app.static_folder = 'static'
    
    bootstrap.init_app(app)
    # mail.init_app(app)
    # moment.init_app(app)
    # db.init_app(app)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
    