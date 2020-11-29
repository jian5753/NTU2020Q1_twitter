from sys import path
from app.main import infunction
from datetime import datetime
from os import pathconf
from typing import OrderedDict
from flask import render_template, session, redirect, url_for
from flask import app
from . import main
from .forms import KeyWordForm, wordStatForm
from . import infunction as inFunc
import pandas as pd
from config import pathConfig
import json
# from .. import db
# from ..models import User

@main.route('/', methods=['GET','POST'])
def index():
    session['articleCnt'], session['twitterRawDf'] = inFunc.jsonFileReader(pathConfig['raw'])
    print(f'============={session["articleCnt"]}==========')

    return (
        render_template('index.html',
            articleCnt=session.get('articleCnt'),
            twitterRawDf = session.get('twitterRawDf')
        )
    )

@main.route('/authorStat', methods= ['GET', 'POST'])
def authorStat():
    form = KeyWordForm()
    tempDF = inFunc.authorStat(pathConfig['woJapFile'])

    if form.validate_on_submit():
        session['keyword'] = form.searchKey.data
        print(session['keyword'])
        tempDF = tempDF.filter(regex=f".*{session['keyword']}.*", axis= 0).sort_index(ascending= True)

    return(
        render_template('authorStat.html',
        authorStatTb = tempDF.head(20).to_html(classes='data'),
        form= form
        )
    )    

@main.route('/wordStat', methods= ['GET', 'POST'])
def wordStat():
    form= wordStatForm()
    tempDF = inFunc.wordStat(pathConfig['woJapFile'], pathConfig['tokenizedFile'])

    if form.validate_on_submit():
        session['authorKey'] = form.searchAuthor.data
        session['rankRange'] = form.rankRange.data
        regexStr = f".*{session['authorKey']}.*"
        tempDF = tempDF[tempDF['author'].str.contains(regexStr, regex=True)]
        tempDF = tempDF[tempDF['rank'] <= session['rankRange']]

    tempDF.drop(columns= ['rank'], inplace= True)
    
    return(
        render_template(
        'wordStat.html',
        wordStatTb= tempDF.head(20).to_html(index= False),
        form= form
        )
    )

@main.route('/clusterAnalysis')
def clusterAnalysis():
    model = inFunc.loadModel(str(pathConfig['w2vModel']))
    circleTable = inFunc.wvCluster(model)

    
    return(
        render_template(
            'cluster.html',
            circleTable= circleTable
        )
    )

@main.route('/topicTag')
def topicTag():
    with open(pathConfig['dataStream'].joinpath('tokenizedLower.json')) as f:
        tokenizedSents = json.load(f)
    f.close()
    circleTb = pd.read_json(pathConfig['dataStream'].joinpath('circleTb.json'), orient= 'split')
    scoreTb = inFunc.grading(tokenizedSents, circleTb)
    print(scoreTb.head())

    print(scoreTb.shape)
    tableLst = []
    for groupN in range(int(scoreTb.shape[1] - 1)):
        colName = f'group_{groupN + 1}'
        view1 = scoreTb[['index', colName]].sort_values(by= colName, ascending= False).iloc[:20]
        rawTb = pd.read_json(pathConfig['woJapFile'], orient= 'split')[['content']].reset_index()
        view2 = view1.merge(rawTb, left_on= 'index', right_on= 'index')
        tableLst.append(view2.to_html(index= False))
    
    return(
        render_template(
            'topicTag.html',
            tableLst = tableLst
       )
    )
