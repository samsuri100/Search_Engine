#!/usr/bin/python3
import string 

class Node():
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

        tokenString = tokenTouple[0]
        if '\n' in tokenString:
            tokenString = tokenString.replace('\n', ' ')

        tokenString = tokenString.translate(str.maketrans('', '', string.punctuation)).lower()
        wordList = tokenString.split(' ')

        wordCountDict = {}
        for word in wordList:
            if (word == ' ') or (word == ''):
                continue
            cleaned = word.strip()
            if cleaned not in wordCountDict:
                wordCountDict[cleaned] = 1
            else:
                wordCountDict[cleaned] += 1

        nodeCount = 0
        for word in sorted(wordCountDict.keys()):
            tempNode = Node(word, wordCountDict[word])
            nodeTail.addNode(tempNode)
            nodeTail = tempNode 
            nodeCount += 1

        self.nodes.append(nodeHead)
        self.numNodes += 1
        self.indivNodeLengths.append(nodeCount)

    def buildPostingsList(self, fileTokenTouples):
        for stringList, fileVal in fileTokenTouples:
            for stringVal in stringList:
                self.addTokenToList((stringVal, fileVal))

    def searchAllBranches(self, term, inverseFlag = False):
        headNodesContainingTerm = []
        term = term.lower()

        for nodeHead in self.nodes:
            avoid = False 
            traversalNode = nodeHead 

            while traversalNode.getNext() != None:
                if traversalNode.getData() == term:
                    if inverseFlag == False:
                        headNodesContainingTerm.append((nodeHead.getData(), nodeHead.getDataFileName()))
                    else:
                        avoid = True 
                    break 
                else:
                    traversalNode = traversalNode.getNext()
                    
            if (inverseFlag == True) & (avoid == False):
                headNodesContainingTerm.append((nodeHead.getData(), nodeHead.getDataFileName()))

        return headNodesContainingTerm

    def inverseAllBranches(self, branches):
        invertedBranches = []

        for nodeHead in self.nodes:
            currentNode = (nodeHead.getData(), nodeHead.getDataFileName())

            if currentNode not in branches:
                invertedBranches.append(currentNode)

        return invertedBranches 
        
    def AND(self, stack1, stack2):
        if isinstance(stack1, list) == False:
            stack1 = self.searchAllBranches(stack1)
        if isinstance(stack2, list) == False:
            stack2 = self.searchAllBranches(stack2)

        return [match for match in stack1 if match in stack2]

    def OR(self, stack1, stack2):
        if isinstance(stack1, list) == False:
            stack1 = self.searchAllBranches(stack1)
        if isinstance(stack2, list) == False:
            stack2 = self.searchAllBranches(stack2)

        return list(set(stack1 + stack2))

    def NOT(self, stack1):
        if isinstance(stack1, list) == False:
            return self.searchAllBranches(stack1, True)
        else:
            return self.inverseAllBranches(stack1)

    def searchIndivTerm(self, term):
        return self.searchAllBranches(term)

    def searchPostingList(self, parsedQuery):
        operatorList = ['not', 'and', 'or']
        operandStack = []
        operatorStack = []

        if (len(parsedQuery) == 1) & (parsedQuery[0] not in operatorList):
                return (1, self.searchIndivTerm(parsedQuery[0]))

        while True:
            if len(parsedQuery) == 0:
                if (len(operatorStack) != 0) & (len(operandStack) != 1):
                    return (0, None)
                else:
                    return (1, operandStack.pop())

            if parsedQuery[-1] not in operatorList:
                operandStack.append(parsedQuery.pop())

            else:
                operatorStack.append(parsedQuery.pop())
                if operatorStack[-1] != 'not':
                    if len(operandStack) >= 2:
                        operator = operatorStack.pop()
                        if operator == 'and':
                            result = self.AND(operandStack.pop(), operandStack.pop())
                        elif operator == 'or':
                            result = self.OR(operandStack.pop(), operandStack.pop()) 
                            
                        operandStack.append(result)
                        
                elif len(operandStack) >= 1:
                    operatorStack.pop()
                    result = self.NOT(operandStack.pop())
                    
                    operandStack.append(result)    

    def printBranches(self):
        for count, node in enumerate(self.nodes):
            print('ON HEAD NODE:', node.getData(), '\nFROM FILE:', node.getDataFileName())
            
            traversalNode = node.getNext()
            print('Branch Data,', str(self.indivNodeLengths[count]), 'in total:')
            while traversalNode != None:
                print(traversalNode.getData())
                traversalNode = traversalNode.getNext()
            print('')
        
    def printResults(self, resultList):
        print('\n-----------------------------------------------')

        if len(resultList) > 1:
            print('FOUND '+str(len(resultList))+' TOTAL RESULTS\n')
        elif len(resultList) == 1:
            print('FOUND '+str(len(resultList))+' TOTAL RESULT\n')
        else:
            print('FOUND '+str(len(resultList))+' TOTAL RESULTS')

        if len(resultList) != 0:
            for count, result in enumerate(resultList):
                print('RESULT '+str(count+1)+':\n'+result[0])
                if count+1 != len(resultList):
                    print('IN FILE:\n'+result[1]+'\n')
                else:
                    print('IN FILE:\n'+result[1])
        
        print('-----------------------------------------------\n')
