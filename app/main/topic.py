from gensim.models import Word2Vec
from gensim.models.keyedvectors import WordEmbeddingSimilarityIndex
import pandas as pd

class Topic():
    def __init__(self, topicName):
        self.topicName = topicName
        self.keyWords = dict()
        self.totalWeight = 0
        self.model = None
        self.relatedWordsDf = None
    
    def compTotalWeight(self):
        self.totalWeight = 0
        for key in self.keyWords:
            self.totalWeight += self.keyWords[key]

    def addKeyWord(self, keyword, weight):
        self.keyWords[keyword] = weight

    def deleteKeyWord(self, keyword):
        self.keyWords.pop(keyword, None)

    def emptySelf(self):
        self.keyWords = dict()

    def loadModel(self, modelPath):
        self.model = Word2Vec.load(modelPath)

    def relatedWords(self):
        view = pd.DataFrame(columns= ['word', 'similarity'])
        for key in self.keyWords:
            temp = pd.DataFrame(self.model.wv.most_similar(key, topn=5), columns=['word', 'similarity'])
            temp = temp.append(pd.DataFrame([[key, 1]], columns = ['word', 'similarity']))
            view = view.append(temp)
        self.relatedWordsDf = pd.DataFrame(view.groupby(by=['word']).max()).sort_values(by= 'similarity', ascending= False)

    def topicRelation(self, sentence):
        scoreDict = self.relatedWordsDf.to_dict()['similarity']
        score = 0
        for word in sentence:
            try:
                score += scoreDict[word]
            except KeyError:
                continue
        if score == 0:
            return 0
        else:
            return score / len(sentence)

