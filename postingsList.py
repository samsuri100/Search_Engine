#!/usr/bin/python3
import string 

class Node(value):
    def __init__(self, value, dataCount = None):
        self.data = value
        self.next = None
        self.dataCount = dataCount 

    def addNode(node2):
        self.next = node2 
         
class PostingsList():
    def __init__(self):
        self.numNodes = 0
        self.indivNodeLengths = []
        self.nodes = []

    def addTokenToList(self, tokenString):
        nodeHead = Node(tokenString) 
        nodeTail = nodeHead 

        tokenString = tokenString.translate(None, string.punctuation)
        wordList = tokenString.split(' ')

        wordCountDict = {}
        for word in wordList:
            if word not in wordCountDict:
                wordCountDict[word] = 1
            else
                wordCountDict[word] += 1

        nodeCount = 0
        for word in sorted(wordCountDict.keys()):
            tempNode = Node(word, wordCountDict[word])
            nodeTail = nodeTail.addNode(tempNode)
            nodeCount += 1

        self.nodes.append(nodeHead)
        self.numNodes += 1
        self.indivNodeLengths.append(nodeCount)
