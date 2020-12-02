import pathlib
import json
from flask.globals import session
import pandas as pd
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from config import pathConfig

def json2df(dirPath):
    print('function called - json2df')
    dataLst = []
    if dirPath.exists():
        for jsonFile in dirPath.glob('*.json'):
            with open(jsonFile, 'r') as jf:
                try:
                    jfData = json.load(jf)
                except:
                    continue
                dataLst.extend(jfData)
            jf.close()

    return pd.DataFrame(dataLst)
     

def allRawGen(rawDirPath):
    allRawDf = json2df(rawDirPath)
    allRawDf.drop(list(range(1, 9)), inplace= True)
    allRawDf.to_json(pathConfig['woJapFile'], orient= 'split')
    
def tokenizedGen():
    allRawDf = pd.read_json(pathConfig['woJapFile'], orient= 'split')
    tweet_tokenizer = TweetTokenizer()
     
    # raw tokenized
    tokenizedLst = []
    for rowNum, rowData in allRawDf.iterrows():
        content = rowData['content']
        tokenizedLst.append(tweet_tokenizer.tokenize(content.lower())) 
        toPrint = str(rowNum)
        print(" " * (10 - len(toPrint)) + toPrint, end='\r')

    # read stop list
    with open(str(pathConfig['stopLst']), 'r') as f:
        stopLst = json.load(f)
    f.close()

    # filter out stop words
    noStopWords = []
    for sentNum, sentence in enumerate(tokenizedLst):
        temp = []
        for word in sentence:
            if not word in stopLst:
                temp.append(word)
        noStopWords.append(temp)        
        toPrint = str(sentNum)
        print(" " * (10 - len(toPrint)) + toPrint, end='\r')
    # output
    with open(str(pathConfig['tokenizedFile']), 'w') as opFile:
        json.dump(noStopWords, opFile)
    opFile.close()

def jsonFileReader(dirPathStr):
    dirPath = pathlib.Path(dirPathStr)
    dataLst = []
    if dirPath.exists():
        for jsonFile in dirPath.glob('*.json'):
            with open(jsonFile, 'r') as jf:
                try:
                    jfData = json.load(jf)
                except:
                    continue
                dataLst.extend(jfData)
            jf.close()

    try:
        articleCnt = len(dataLst)
        twitterRawDf = pd.DataFrame(dataLst).sample(n= 15).to_html(classes='data')
    except:
        twitterRawDf = pd.DataFrame()
    return articleCnt, twitterRawDf

def authorStat(filePath):
    allRaw = pd.read_json(filePath, orient= 'split')
    contentCntByAuthor = allRaw.groupby(by= 'author').count()[['content']]
    contentCntByAuthor.sort_values(by= 'content', ascending= False)
    print(contentCntByAuthor.columns)
    return contentCntByAuthor


def wordStat(filePath1, filePath2):
    stopwordLst = stopwords.words('english')
    allRaw = pd.read_json(filePath1, orient= 'split')
    tokenizedTb = pd.read_json(filePath2, orient= 'split')
    view1 = tokenizedTb.join(allRaw.reset_index()[['index', 'author']], on='index', rsuffix= '_words')
    view2 = view1[view1['pos_tag'].isin(['NN', 'NNP', 'NNS', 'NNPS'])]
    view2 = view2[~view2['word'].isin(stopwordLst)].groupby(by= ['author', 'word'])
    view3 = view2.count()[['wordCnt']].sort_values(by= ['author', 'wordCnt'], ascending= False)
    view3['rank'] = view3.groupby(by= ['author']).rank(ascending= False)
    view3.reset_index(inplace=True)
    return(view3)

def loadModel(filePath):
    return Word2Vec.load(filePath)

def wvCluster(wvModel, clusterCnt = 4):
    kMeansModel = KMeans(n_clusters= clusterCnt)
    kMeansModel.fit(wvModel.wv.vectors)

    similarLst= []
    for center in kMeansModel.cluster_centers_:
        similarLst.append(wvModel.most_similar([center], topn= 20))

    similarWordTb = pd.DataFrame(similarLst[0], columns = ['group_1', 'similarity_1'])
    for i, circle in enumerate(similarLst[1:]):
        temp = pd.DataFrame(circle, columns = [f'group_{i+2}', f'similarity_{i+2}'])
        similarWordTb = similarWordTb.merge(temp, left_index= True, right_index= True)

    similarWordTb.to_json(pathConfig['circleTb'], orient= 'split')
    return similarWordTb.to_html()

def grading(tokenizedLst, circleTb):
    clusterCnt = int(circleTb.shape[1] / 2)
    scoreDict = dict()
    for i in range(clusterCnt):
        currentGp = f'group_{i+1}'
        gradingDict = circleTb.iloc[:, 2 * i: 2 * (i + 1)].set_index(currentGp).to_dict()
        gradingDict = gradingDict[f'similarity_{i+1}']
        scoreDict[currentGp] = []
        for sentence in tokenizedLst:
            score = 0
            for word in sentence:
                try:
                    score += gradingDict[word]
                except KeyError:
                    continue
            scoreDict[currentGp].append(score / len(session))
    scoreTb = pd.DataFrame(scoreDict).reset_index()
    return scoreTb
    


def wordToVec_train(sentences):
    model = Word2Vec(sentences= sentences)

