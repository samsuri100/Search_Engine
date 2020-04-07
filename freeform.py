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

    #Function builds initial Tf-Idf Matrix or recalculates Tf-Idf Matrix
    #If rebuildFlag is False: building Tf-Idf Matrix for the first time
    #If rebuildFlag is True: rebuilding Tf-Idf Matrix to expand matrix vocabulary 
    def buildMatrix(self, fileTouples, rebuildFlag = False, newDoc = None):
        #Being built for the first time
        if rebuildFlag == False:
            #Tuple in format: [([text1,...,textN], file1),...,([text1,...,textN], fileN)]
            for touple in fileTouples:
                for text in touple[0]:
                    self.mappedFileList.append(touple[1])
                    self.documentList.append(text)
                    self.documentIndex += 1

        #If user query has vocabulary not in Tf-Idf Matrix, add it to document list, recalculate Tf-Idf Matrix
        else:
            self.documentList.append(newDoc)

        tfidfVect = TfidfVectorizer()
        #Tf-Idf Matrix
        self.tfidfMatrix = tfidfVect.fit_transform(self.documentList)
        #Matrix has tokenized words of documentsList as columns
        self.vocabulary = tfidfVect.get_feature_names()

        #Rebuilt with query to expand vocabulary, we dont want query to be returned to user though
        #Remove query row from Tf-Idf Matrix, but not document list, else some vocabulary may be lost in future when rebuilding
        if rebuildFlag == True:
            self.tfidfMatrix = self.tfidfMatrix[:self.documentIndex, :]

    #Function searches Tf-Idf Matrix for free-form query
    #May re-compute Tf-Idf Matrix if it lacks vocabulary to compute query
    def searchMatrix(self, freeQueryText):
        #Using nltk's word_tokenize
        tokenizedQuery = word_tokenize(freeQueryText)

        #Removing punctuation from word_tokenize list
        #If word contains '-', such as '1996-1997', split apart, so ['1996', '1997'] and add to list
        cleanedTokenized = []
        for word in tokenizedQuery:
            #Removing punctuation
            if word not in string.punctuation:
                #Spliting apart words with '-' in them
                if '-' in word:
                    cleanedTokenized += word.split('-') 
                else:
                    cleanedTokenized.append(word)

        #If a word in query is not present in Tf-Idf Matrix vocabulary, it must be recalculated
        rebuildFlag = 0
        for word in cleanedTokenized:
            if word not in self.vocabulary:
                rebuildFlag = 1
                break

        #Rebuilding Tf-Idf Matrix with user query if needed
        if rebuildFlag == 1:
            self.buildMatrix(None, True, freeQueryText)

        #Building Tf-Idf Matrix only for the query itself, dimensions are 1 x n, where n = len(vocabulary)
        queryVect = TfidfVectorizer(vocabulary = self.vocabulary)
        queryMatrix = queryVect.fit_transform([freeQueryText])

        #Searching by cosine similarities
        cosSim = cosine_similarity(queryMatrix, self.tfidfMatrix)[0]
        #Getting indexes to sort list
        index = cosSim.argsort()

        #If cosine similarity score is 0, ignore, else add index to result list
        useIndex = []
        for count, num in enumerate(cosSim):
            if num != 0:
                useIndex.append(index[count])

        return useIndex 

    #Function prints free-form search results for the user
    def printResults(self, indexList, fileTouplesResults, equalBool, resultLimit):
        #indexList is sorted in order of increasing probability, ie: [least likely match,...,most likely match]
        #If user applies result limit, only get top # of results
        useIndex = list(reversed(indexList))[:resultLimit]
        
        #Search specificity may be different than result specificity
        #This means you can search for the most relevent sentences, but want the paragraph each sentence occurs in
        fileResultChunks = []
        #If '-specificity' and '-result' are the same, don't have to recompute list
        if equalBool == 0:
            #Tuple in format: [([text1,...,textN], file1),...,([text1,...,textN], fileN)]
            for touple in fileTouplesResults:
                for text in touple[0]:
                    fileResultChunks.append(text)

        print('\n-----------------------------------------------')

        #Different versions to be grammatically correct
        if len(useIndex) > 1:
            print('FOUND '+str(len(useIndex))+' TOTAL RESULTS\n')
        elif len(useIndex) == 1:
            print('FOUND '+str(len(useIndex))+' TOTAL RESULT\n')
        else:
            print('FOUND '+str(len(useIndex))+' TOTAL RESULTS') 

        #If results are found
        if len(useIndex) != 0:
            for count, index in enumerate(useIndex):
                #Printing text according to '-specificity'
                print('RESULT '+str(count+1)+':\n'+self.documentList[index])
                #If '-specificity' and '-result' are the same, don't display the same thing twice
                #ie: 'found {sentence} in {paragraph}' is fine, but 'found {sentence} in {sentence}' is not 
                if equalBool == 0:
                    #Printing where 'specificity' text is in larger 'result' text
                    for text in fileResultChunks:
                        if self.documentList[index] in text:
                            print('FOUND IN:\n'+text)
                            break 
                #Printing the file the text is in
                if count+1 != len(useIndex):
                    print('IN FILE:\n'+self.mappedFileList[index]+'\n')
                #Last element lacks newline character for appearance
                else:
                    print('IN FILE:\n'+self.mappedFileList[index])

        print('-----------------------------------------------\n')
