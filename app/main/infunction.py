import pathlib
import json
import pandas as pd

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
        twitterRawDf = pd.DataFrame(dataLst).to_html(classes='data')
    except:
        twitterRawDf = pd.DataFrame()
    return articleCnt, twitterRawDf

