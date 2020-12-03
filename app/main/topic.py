from gensim.models import Word2Vec


class Topic():
    def __init__(self, topicName):
        self.topicName = topicName
        self.keyWords = dict()
        self.totalWeight = 0
    
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

    def topicRelation(self):
        for key in self.keyWords:
            print(self.model.wv.most_similar(key))