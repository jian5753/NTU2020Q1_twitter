from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .infunction import jsonFileReader
# from .. import db
# from ..models import User

@main.route('/', methods=['GET','POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():
        session['dirPath']=form.dataLocation.data
        session['articleCnt'], session['twitterRawDf'] = jsonFileReader(session['dirPath'])
        print(f'============={session["articleCnt"]}==========')
        return redirect(url_for('.index'))

    return (
        render_template('index.html',
            form=form, 
            name=session.get('dirPath'), 
            articleCnt=session.get('articleCnt'),
            twitterRawDf = session.get('twitterRawDf')
        )
    )
