#!/usr/bin/python3
import string 

class Node(value):
    def __init__(self, value, dataCount = None, fileName = None):
        self.data = value
        self.dataFileName = fileName
        self.next = None
        self.dataCount = dataCount 

    def addNode(self, node2):
        self.next = node2

    def getNext(self):
        return self.next 

    def getData(self):
        return self.data 

    def getDataFileName(self):
        return self.dataFileName 
         
class PostingsList():
    def __init__(self):
        self.numNodes = 0
        self.indivNodeLengths = []
        self.nodes = []

    def addTokenToList(self, tokenTouple):
        nodeHead = Node(tokenTouple[0], None, tokenTouple[1]) 
        nodeTail = nodeHead 

        tokenString = tokenString.translate(str.maketrans('', '', string.punctuation).lower()
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

    def buildPostingList(self, fileTokenTouples):
        for touple in fileTokenTouples:
            self.addTokenToList(touple)

    def searchAllBranches(self, term, inverseFlag = False):
        headNodesContainingTerm = []
        term = term.lower()

        for nodeHead in self.nodes:
            avoid = False 
            traversalNode = nodeHead 

            while traversalNode.getNext() != None:
                if traversalNode.getData() == term:
                    if inverseFlag == False:
                        headNodesContainingTerm.append((nodeHead.getData(), nodeHead.getFileName())
                    else:
                        avoid = True 
                    break 
                else:
                    traversalNode = traversalNode.getNext()
                    
            if (inverseFlag == True) & (avoid == False):
                headNodesContainingTerm.append(nodeHead.getData(), nodeHead.getFileName())

        return headNodesContainingTerm

    def inverseAllBranches(self, branches):
        invertedBranches = []

        for nodeHead in self.nodes:
            currentNode = (nodeHead.getData(), nodeHead.getFileName())

            if currentNode not in branches:
                invertedBranches.append(currentNode)
        
    def AND(self, stack1, stack2):
        if (len(stack1)) == 1 & (type(stack1[0]) == str):
            stack1 = self.searchAllBranches(stack1[0])
        if (len(stack2)) == 1 & (type(stack2[0]) == str):
            stack2 = self.searchAllBranches(stack2[0])

        return [match for match in stack1 if match in stack2]

    def OR(self, stack1, stack2):
        if (len(stack1)) == 1 & (type(stack1[0]) == str):
            stack1 = self.searchAllBranches(stack1[0])
        if (len(stack2)) == 1 & (type(stack2[0]) == str):
            stack2 = self.searchAllBranches(stack2[0])

        return list(set(stack1 + stack2))

    def NOT(self, stack1):
        if (len(stack1)) == 1 & (type(stack1[0]) == str):
            return self.searchAllBranches(stack1[0], True)
        else:
            return self.inverseAllBranches(stack1)

    def searchPostingList(self, parsedQuery):
        operatorList = ['NOT', 'AND', 'OR']
        operandStack = []
        operatorStack = []

        while True:
            if len(parsedQuery) == 0:
                if (len(operatorStack) != 0) & (len(operandStack) != 1):
                    return (0, None)
                elese:
                    return (1, operandStack.pop())

            if parsedQuery[-1] not in operatorList:
                operandStack.append(parsedQuery.pop())

            else:
                operatorStack.append(parsedQuery.pop())
                if operatorStack[-1] != 'NOT':
                    if len(operandStack) >= 2:
                        operator = operatorStack.pop()
                        if operator == 'AND':
                            result = self.AND(operandStack.pop(), operandStack.pop())
                        elif operator == 'OR':
                            result = self.OR(operandStack.pop(), operandStack.pop()) 
                            
                        operandStack.append(result)
                        
                elif len(operandStack) >= 1:
                    operatorStack.pop()
                    result = self.NOT(operandStack.pop())
                    
                    operandStack.append(result)    
        
    def printResults(self, resultList):
        
