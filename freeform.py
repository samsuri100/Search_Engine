#!/usr/bin/python3
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class FreeForm():
    def __init__(self):
        self.tfidfMatrix = None
        self.mappedFileList = []
        self.documentList = []
        self.vocabulary = []

    def buildMatrix(self, fileTouples, rebuildFlag = False, newDoc = None):
        if rebuildFlag == False:
            for touple in fileTouples:
                for text in touple[0]:
                    self.mappedFileList.append(tuple[1])
                    self.documentList.append(text)
        else:
            self.documentList.append(newDoc)

        tfidfVect = TfidfVectorizer()
        self.tfidfMatrix = tfidfVect.fit_transform(self.documentList)
        self.vocabulary = tfidfVect.get_feature_names()

        if rebuildFlag == True:
            self.tfidfMatrix = self.tfidfMatrix[:-1, :]
            self.documentList.pop()

    def searchMatrix(self, freeQueryText):
        tokenizedQuery = word_tokenize(freeQueryText)

        cleanedTokenized = []
        for word in tokenizedQuery:
            if word not in string.punctuation:
                if '-' in word:
                    cleanedTokenized += word.split('-') 
                else:
                    cleanedTokenized.append(word)

        rebuildFlag = 0
        for word in cleanedTokenized:
            if word not in self.vocabulary:
                rebuildFlag = 1
                break

        if rebuildFlag == 1:
            self.buildMatrix(None, True, freeQueryText)

        queryVect = TfidfVectorizer(vocabulary = self.vocabulary)
        queryMatrix = queryVect.fit_transform(freeQueryText)

        cosSim = cosine_similarity(queryMatrix, self.tfidfMatrix)[0]
        index = cosSim.argsort()

        useIndex = []
        for count, num in enumerate(cosSim):
            if num != 0:
                useIndex.append(index[count])

        return useIndex 

    def printResults(self, indexList):
        mostSimilarFirstIndex = list(reversed(useIndex))

        print('\n-----------------------------------------------')
        if len(indexList) > 1:
            print('FOUND '+str(len(indexList))+' TOTAL RESULTS\n')
        elif len(indexList) == 1:
            print('FOUND '+str(len(indexList))+' TOTAL RESULT\n')
        else:
            print('FOUND '+str(len(indexList))+' TOTAL RESULTS') 

        if len(indexList) != 0:
            for index in useIndex:
                print(
        print('-----------------------------------------------\n')




