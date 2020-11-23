import pathlib
import json
import pandas as pd
from nltk.corpus import stopwords

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
