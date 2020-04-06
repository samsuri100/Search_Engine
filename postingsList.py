#!/usr/bin/python3
import string 

class Node():
    def __init__(self, value, dataCount = None, fileName = None):
        self.data = value
        self.dataFileName = fileName
        self.next = None
        self.dataCount = dataCount 

    #Function points current node to another node
    def addNode(self, node2):
        self.next = node2

    #Getter function for next
    def getNext(self):
        return self.next 

    #Getter function for data
    def getData(self):
        return self.data 

    #Getter function for dataFileName
    def getDataFileName(self):
        return self.dataFileName 
         
class PostingsList():
    def __init__(self):
        self.numNodes = 0
        self.indivNodeLengths = []
        self.nodes = []

    #Function adds a string to the postings list as a branch
    def addTokenToList(self, tokenTouple):
        #Creating linked list head
        #Text added to Node.data contains punctuation, newline characters, spaces
        #Allows text, in its entirety, to be displayed to user if matched
        nodeHead = Node(tokenTouple[0], None, tokenTouple[1]) 
        nodeTail = nodeHead 

        #Postings have newline characters, spaces, punctuation removed
        #Replacing newline characters with spaces
        tokenString = tokenTouple[0]
        if '\n' in tokenString:
            tokenString = tokenString.replace('\n', ' ')

        #Removing punctuation from string
        #Lowercasing string
        tokenString = tokenString.translate(str.maketrans('', '', string.punctuation)).lower()
        wordList = tokenString.split(' ')

        #Not adding spaces or empty strings as postings
        wordCountDict = {}
        for word in wordList:
            if (word == ' ') or (word == ''):
                continue
            cleaned = word.strip()
            #Though this is a boolean retrieval matrix
            #incrementing counter allows for 'ordering results' functionality to be added later
            if cleaned not in wordCountDict:
                wordCountDict[cleaned] = 1
            else:
                wordCountDict[cleaned] += 1

        nodeCount = 0
        #Sorting postings, allows for more efficent search when looking for a search term
        #Adding each posting to head node in linked list
        for word in sorted(wordCountDict.keys()):
            tempNode = Node(word, wordCountDict[word])
            nodeTail.addNode(tempNode)
            nodeTail = tempNode 
            nodeCount += 1

        self.nodes.append(nodeHead)
        #Storing some metadata on each branch, allows for further functionality in the future
        self.numNodes += 1
        self.indivNodeLengths.append(nodeCount)

    #Function builds postings list from list of tuples
    #Tuples in format: [([Text1,...,TextN], file1),...,([Text1,...,TextN], fileN)]
    def buildPostingsList(self, fileTokenTouples):
        for stringList, fileVal in fileTokenTouples:
            for stringVal in stringList:
                #Every string has a file associated with it when passed to branch building function
                self.addTokenToList((stringVal, fileVal))

    #Function searches postings list for an individual search term, ie: 'cat'
    #If inverseFlag=False, find all node heads whose postings contain 'cat'
    #If inverseFlag=True, find all node heads whose postings do not contain 'cat'
    def searchAllBranches(self, term, inverseFlag = False):
        headNodesContainingTerm = []
        #All search is done on lowercase search terms
        term = term.lower()
    
        #Iterating over postings list
        for nodeHead in self.nodes:
            avoid = False 
            traversalNode = nodeHead 
    
            #Iterating over branches
            while traversalNode.getNext() != None:
                if traversalNode.getData() == term:
                    #Inverse flag is disabled, if search term is found, include node data and file name info
                    if inverseFlag == False:
                        headNodesContainingTerm.append((nodeHead.getData(), nodeHead.getDataFileName()))
                    else:
                        avoid = True 
                    break 
                else:
                    traversalNode = traversalNode.getNext()
            
            #Inverse flag is true, end of branch was reached, include node data and file name info
            if (inverseFlag == True) & (avoid == False):
                headNodesContainingTerm.append((nodeHead.getData(), nodeHead.getDataFileName()))

        return headNodesContainingTerm

    #Function invertes list of node head data, finds all node heads that are not in passed-in list
    def inverseAllBranches(self, branches):
        invertedBranches = []

        #Iterating over postings list
        for nodeHead in self.nodes:
            currentNode = (nodeHead.getData(), nodeHead.getDataFileName())

            #Current node is not a node in passed in list, include this node
            if currentNode not in branches:
                invertedBranches.append(currentNode)

        return invertedBranches 
        
    #Function applies 'AND' operator to search term or list of node head data
    def AND(self, stack1, stack2):
        #If stack1 is a string, ie: 'cat', get node head result list for that term
        if isinstance(stack1, list) == False:
            stack1 = self.searchAllBranches(stack1)
        #If stack2 is a string, ie: 'cat', get node head result list for that term
        if isinstance(stack2, list) == False:
            stack2 = self.searchAllBranches(stack2)

        #stack1 and stack2 might already be lists
        #Returns elements found in both stack1 and stack2
        return [match for match in stack1 if match in stack2]

    #Function applies 'OR' operator to search term or list of node head data
    def OR(self, stack1, stack2):
        #If stack1 is a string, ie: 'cat', get node head result list for that term
        if isinstance(stack1, list) == False:
            stack1 = self.searchAllBranches(stack1)
        #If stack2 is a string, ie: 'cat', get node head result list for that term
        if isinstance(stack2, list) == False:
            stack2 = self.searchAllBranches(stack2)

        #stack1 and stack2 might already be lists
        #Simply add lists and remove duplicate strings
        return list(set(stack1 + stack2))

    #Function applies 'NOT' operator to search term or list of node head data
    def NOT(self, stack1):
        #If stack1 is a string, ie: 'cat'
        #Search postings list for individual term, but 'True' flag inverts results
        if isinstance(stack1, list) == False:
            return self.searchAllBranches(stack1, True)
        #If stack1 is a list of node head data, find all other node heads not in this list
        else:
            return self.inverseAllBranches(stack1)

    #Function searches for individual search term in postings list, ie: 'cat'
    def searchIndivTerm(self, term):
        return self.searchAllBranches(term)

    #Function uses prefix list of boolean operations and search terms to search postings list
    #Returns tuple in format: 
    #({0 or 1, 0 if search is invalid, 1 if search is valid}, [strings of matching head nodes in postings list])
    def searchPostingList(self, parsedQuery):
        operatorList = ['not', 'and', 'or']
        operandStack = []
        operatorStack = []

        #If prefix list is a single search time, ie: ['cat']
        if (len(parsedQuery) == 1) & (parsedQuery[0] not in operatorList):
                return (1, self.searchIndivTerm(parsedQuery[0]))

        while True:
            if len(parsedQuery) == 0:
                #When prefix list is empty, operator stack has to be 0, operand stack has to be 1
                if (len(operatorStack) != 0) & (len(operandStack) != 1):
                    return (0, None)
                else:
                    return (1, operandStack.pop())

            #If prefix element is operand, add to operand stack
            if parsedQuery[-1] not in operatorList:
                operandStack.append(parsedQuery.pop())

            #Prefix element is operator
            else:
                #Adding to operator stack
                operatorStack.append(parsedQuery.pop())
                #'NOT' operator operates on single operand
                #'OR' & 'AND' operators operate on two operands
                if operatorStack[-1] != 'not':
                    #At least two operands
                    if len(operandStack) >= 2:
                        operator = operatorStack.pop()
                        if operator == 'and':
                            result = self.AND(operandStack.pop(), operandStack.pop())
                        elif operator == 'or':
                            result = self.OR(operandStack.pop(), operandStack.pop()) 
                        #Re-adding result to operand stack    
                        operandStack.append(result)

                #At least one operand
                elif len(operandStack) >= 1:
                    operatorStack.pop()
                    result = self.NOT(operandStack.pop())
                    
                    #Re-adding result to operand stack
                    operandStack.append(result)    

    #Function is used for debugging, iterates over postings list
    #At each iteration, prints node head data and iterates over each branch, printing postings
    def printBranches(self):
        for count, node in enumerate(self.nodes):
            #Printing node head data
            print('ON HEAD NODE:', node.getData(), '\nFROM FILE:', node.getDataFileName())
            
            #Traversing branches
            traversalNode = node.getNext()
            print('Branch Data,', str(self.indivNodeLengths[count]), 'in total:')

            #Printing postings
            while traversalNode != None:
                print(traversalNode.getData())
                traversalNode = traversalNode.getNext()
            print('')
        
    #Function prints results of boolean search query for the user
    def printResults(self, resultList):
        print('\n-----------------------------------------------')

        #Different versions to be gramatically correct
        if len(resultList) > 1:
            print('FOUND '+str(len(resultList))+' TOTAL RESULTS\n')
        elif len(resultList) == 1:
            print('FOUND '+str(len(resultList))+' TOTAL RESULT\n')
        else:
            print('FOUND '+str(len(resultList))+' TOTAL RESULTS')

        if len(resultList) != 0:
            for count, result in enumerate(resultList):
                #Printing text
                print('RESULT '+str(count+1)+':\n'+result[0])

                #Printing file text was found in
                if count+1 != len(resultList):
                    print('IN FILE:\n'+result[1]+'\n')
                #Last element lacks newline character for appearance
                else:
                    print('IN FILE:\n'+result[1])
        
        print('-----------------------------------------------\n')
