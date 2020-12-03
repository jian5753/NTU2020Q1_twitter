from flask import render_template, session, redirect
from gensim.models.word2vec import Word2Vec
from . import main
from .forms import KeyWordForm, wordStatForm, NewTopicForm, EditTopicForm, DeleteTopicForm
from . import infunction as inFunc
from . import topic
import pandas as pd
from config import pathConfig
import json
import pickle
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

@main.route('/dataManagement', methods = ['GET', 'POST'])
def dataManagement():
    rawDataPath = pathConfig['raw']
    ifRawExists = rawDataPath.exists()
    ifTokenizedExists = pathConfig['tokenizedFile'].exists()
    return(
        render_template(
            'dataManagement.html',
            rawDataPath = rawDataPath,
            ifRawExists = ifRawExists,
            tokenizedDataPath = pathConfig['tokenizedFile'],
            ifTokenizedExists = ifTokenizedExists,
            stopLstPath = pathConfig['stopLst'],
            ifStopLstExists = pathConfig['stopLst'].exists()
        )
    )


@main.route('/dataManagement/refresh', methods = ['GET', 'POST'])
def dataFlowRefresh():
    print(len(list(pathConfig['raw'].glob("*.json"))))
    inFunc.allRawGen(pathConfig['raw'])
    inFunc.tokenizedGen()

    return redirect('/dataManagement')

@main.route('/dataManagement/retrain', methods = ['GET', 'POST'])
def wvModelRetrain():
    with open(str(pathConfig['tokenizedFile']), 'r') as f:
        sentences = json.load(f)
    f.close()
    model = Word2Vec(sentences= sentences)
    model.save(str(pathConfig['w2vModel'])) 
    return redirect('/dataManagement')
@main.route('/topicManagement', methods = ['GET'])
def topicManagement():
    topicPathLst = list(pathConfig['modelFolder'].glob('*.topic'))
    topicLst = []
    for path in topicPathLst:
        with open(str(path), 'rb') as f:
            obj = pickle.load(f)
            tempDict = dict()
            tempDict[obj.topicName] = obj.keyWords
            topicLst.append(tempDict)
        f.close()

    
    return(
        render_template(
            '/topicManagement.html',
            topicLst= topicLst
        )
    )
@main.route('/topicManagement/addTopic', methods = ['GET', 'POST'])
def topics():
    form = NewTopicForm()

    if form.validate_on_submit():
        topicName = form.topicName.data
        test = topic.Topic(topicName)
        #test.addKeyWord('covid', 1)
        #test.topicRelation()
        opPath = str(pathConfig['modelFolder'].joinpath(f'{topicName}.topic'))
        
        with open(opPath, 'wb') as f:
            pickle.dump(test, f)
        f.close()
        return redirect('/topicManagement/addTopic')
    
    return(
        render_template(
            'topic_add.html',
            form= form
        )
    )
@main.route('/topicManagement/edit', methods = ['GET', 'POST'])
def topicEditor():
    form = EditTopicForm()
    form.topicToEdit.choices = [x.stem for x in list(pathConfig['modelFolder'].glob('*.topic'))]

    if form.validate_on_submit():
        # load topic obj pickle
        topicName = form.topicToEdit.data
        topicObjPath = list(pathConfig['modelFolder'].glob(f'{topicName}.topic'))[0]

        with open(str(topicObjPath), 'rb') as f:
            targetTopic = pickle.load(f)
        f.close()
        
        # add new key words
        newKeyWords = form.newKeyWord.data.split(', ')
        print(newKeyWords)
        weightLst = form.keyWordWeight.data.split(', ')
        for i, keyword in enumerate(newKeyWords):
            weight = int(weightLst[i])
            targetTopic.addKeyWord(keyword, weight)

        # save changes
        with open(str(topicObjPath), 'wb') as f:
            pickle.dump(targetTopic, f)
        f.close()

    return(
        render_template(
            'topic_edit.html',
            form = form
        )
    )

@main.route('/topicManagement/delete', methods= ['GET', 'POST'])
def deleteTopic():
    form = DeleteTopicForm()
    form.topicToDel.choices = [(x.stem, x.stem) for x in list(pathConfig['modelFolder'].glob('*.topic'))]

    if form.validate_on_submit():
        selected = form.topicToDel.data
        for topicName in selected:
            topicObjPath = list(pathConfig['modelFolder'].glob(f'{topicName}.topic'))[0]
            with open(str(topicObjPath), 'rb') as f:
                targetTopic = pickle.load(f)
            f.close()
            targetTopic.emptySelf()

            with open(str(topicObjPath), 'wb') as f:
                pickle.dump(targetTopic, f)
            f.close() 
    return(
        render_template(
            'topic_delete.html',
            form = form
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
