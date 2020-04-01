#!/usr/bin/python3
import string
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class FreeForm():
    def __init__(self):
        self.tfidfMatrix = None
        self.mappedFileList = []
        self.documentList = []
        self.vocabulary = []
        self.documentIndex = 0

    def buildMatrix(self, fileTouples, rebuildFlag = False, newDoc = None):
        if rebuildFlag == False:
            for touple in fileTouples:
                for text in touple[0]:
                    self.mappedFileList.append(touple[1])
                    self.documentList.append(text)
                    self.documentIndex += 1
        else:
            self.documentList.append(newDoc)

        tfidfVect = TfidfVectorizer()
        self.tfidfMatrix = tfidfVect.fit_transform(self.documentList)
        self.vocabulary = tfidfVect.get_feature_names()

        if rebuildFlag == True:
            self.tfidfMatrix = self.tfidfMatrix[:self.documentIndex, :]

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
        queryMatrix = queryVect.fit_transform([freeQueryText])

        cosSim = cosine_similarity(queryMatrix, self.tfidfMatrix)[0]
        index = cosSim.argsort()

        useIndex = []
        for count, num in enumerate(cosSim):
            if num != 0:
                useIndex.append(index[count])

        return useIndex 

    def printResults(self, indexList, fileTouplesResults, equalBool, resultLimit):
        useIndex = list(reversed(indexList))[:resultLimit]

        fileResultChunks = []
        if equalBool == 0:
            for touple in fileTouplesResults:
                for text in touple[0]:
                    fileResultChunks.append(text)

        print('\n-----------------------------------------------')

        if len(useIndex) > 1:
            print('FOUND '+str(len(useIndex))+' TOTAL RESULTS\n')
        elif len(useIndex) == 1:
            print('FOUND '+str(len(useIndex))+' TOTAL RESULT\n')
        else:
            print('FOUND '+str(len(useIndex))+' TOTAL RESULTS') 

        if len(useIndex) != 0:
            for count, index in enumerate(useIndex):
                print('RESULT '+str(count+1)+':\n'+self.documentList[index])
                if equalBool == 0:
                    for text in fileResultChunks:
                        if self.documentList[index] in text:
                            print('FOUND IN:\n'+text)
                            break 
                print('IN FILE:\n'+self.mappedFileList[index]+'\n')

        print('-----------------------------------------------\n')
