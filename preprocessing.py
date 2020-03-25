#!/usr/bin/python3
import re 
from nltk.tokenize import sent_tokenize

def multParCheckValue(flag):
    if flag == 'specificity':
        multParLength = input("Please enter multi-paragraph length for '-specificity': ")
    else:
        multParLength = input("Please enter multi-paragraph length for '-results': ")
    while (multParLength.isdigit() == False):
        multParLength = input('Please enter a valid integer: ')
    multParLength = int(multParLength)

class Preprocessing():
    def __init__(self, specificity, fileName):
        specificity = specificity 
        fileName = fileName 
        fileContents = None
        tokenizedList = None

    def readFile(self):
        with open(self.fileName, 'r') as openFile:
            self.fileContents = openFile.read()

    def tokenizeText(self):
        if self.specificity == 0:
            self.tokenizedList = sent_tokenize(self.fileContents)

        elif self.specificity == 1:
            self.tokenizedList = self.fileContents.split('\n\n')

        else:
            paragraphList = self.fileContents.split('\n\n')

            tempParStr = ''
            for count, pargraph in enumerate(paragraphList):
                tempParStr += pargraph + '\n\n'
                if (counter+1) % self.specificity == 0:
                    self.tokenizedList.append(tempParStr[:-4])
                    tempParStr = ''

    def normalizeTokens(self):
        for count, token in enumerate(self.tokenizedList):
            self.tokenizedList[count] = token.lower()

    def checkQueryParenthesis(queryString):
        begParenCount = 0
        endParenCount = 0

        for character in queryString:
            if character == '(':
                begParenCount += 1
            elif character == ')':
                endParenCount += 1

        if begParenCount == endParenCount:
            return True 
        else:
            return False 

    def convertToPrefixFromInfix(queryString):
        priorityMap = {'AND': 1, 'OR': 1, 'NOT': 1, '(': 0, ')':0}
        operators = ['AND', 'OR', 'NOT', '(', ')']
        prefix = []
        stack = []

        splitQuery = list(filter(lambda x: (x != ' ') & (x != ''), re.split('(\W)', queryString)))
        reversedQuery = list(reversed(splitQuery))

        for term in reversedQuery:
            if term not in operators:
                prefix.append(term)
            elif term == ')':
                stack.append(term)
            elif term == '(':
                x = stack[-1]
                while x != ')':
                    prefix.append(stack.pop()) 
                    x = stack[-1]
                stack.pop()
            else:
                if len(stack) == 0:
                    stack.append(term)
                else:
                    while True:
                        if priorityMap[term] >= priorityMap[stack[-1]]:
                            stack.append(term)
                            break
                        else:
                            prefix += stack.pop()
        while len(stack) > 0:
            prefix += stack.pop()

        return list(reversed(prefix))

    def parseQuery(self):
        while True:
            toParse = input("Please enter you boolean logic query, input 'example' \n\
                             to see previous examples or 'help' for syntax clarification: ")

            if toParse == 'example':
                print("Example 1: NOT(cat AND dog) OR bird")
                print("Example 2: google AND NOT(apple) AND 95050")

            if toParse == 'help':
                print('''
                        Allowed operators: NOT, AND, OR \n \
                        Operators may be capitalized or lowercase \n \
                        
                        Parenthesis and nested parenthesis are allowed
                        Words are numbers are allowed 
                        
                        Words, even proper nouns, with a space must be joined with an operator
                        Example: San AND Francisco
                     '''
            else:
                result = checkQueryParenthesis(toParse)
                if result == False:
                    print('Query is not valid, mismatching parenthesis')
                else:
                   prefixQS = convertToPrefixFromInfix(toParse)
                   
