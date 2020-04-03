#!/usr/bin/python3
import re
from nltk.tokenize import sent_tokenize

#Function gets user input for multi-paragraph length for either '-specificity' or '-result' flags
def multParCheckValue(flag):
    #'multi-paragraph' was entered for '-specificity' flag
    if flag == 'specificity':
        multParLength = input("Please enter multi-paragraph length for '-specificity': ")
    #'multi-paragraph' was entered for '-result' flag
    else:
        multParLength = input("Please enter multi-paragraph length for '-results': ")
    #Ensuring input is a valid integer
    while (multParLength.isdigit() == False):
        multParLength = input('Please enter a valid integer: ')
    
    print('')
    return int(multParLength)

class Preprocessing():
    def __init__(self, specificity = None, fileName = None):
        self.specificity = specificity 
        self.fileName = fileName 
        self.fileContents = None
        self.tokenizedList = []

    #Function reads contents of .txt files
    def readFile(self):
        with open(self.fileName, 'r') as openFile:
            self.fileContents = openFile.read()

    #Function tokenizes text either by sentence, paragraph, or user defined multi-paragraph length
    def tokenizeText(self):
        #Using nltk's sent_tokenize to tokenize by sentence
        #Automatically handles white space and newline characters
        if self.specificity == 0:
            self.tokenizedList = sent_tokenize(self.fileContents)

        #Tokenizing by paragraph
        elif self.specificity == 1:
            #Spliting based on newline characters
            splitList = self.fileContents.split('\n')
            for term in splitList:
                #If multiple newline characters between paragraphs, extra ones are discarded
                if (term != ' ') and (term != ''):
                    #Stripping paragraphs incase there is a space after last period
                    self.tokenizedList.append(term.strip())

        #Tokenizing by multi-paragraph
        else:
            #Splitlines will group newline character immediately after text with the text
            #Immediately sequential newline characters after this are tokenized separately
            #ie: 'Hello\n\n\n'.splitlines(keepends=True) -> ['Hello\n', '\n', '\n']
            paragraphList = self.fileContents.splitlines(keepends=True)

            tempParStr = ''
            paragraphCount = 0
            for text in paragraphList:
                #If on text, which ends with a newline character, this is a paragraph
                if (text[-1] == '\n') & (text[0] != '\n'):
                    paragraphCount += 1
                #Immediately sequential newline characters are added to string, does not affect paragraph count
                tempParStr += text 
                #If number of paragraphs in tempParStr is equal to user defined multi-paragraph length, add to token list
                if paragraphCount == self.specificity:
                    self.tokenizedList.append(tempParStr.strip())
                    tempParStr = ''
                    paragraphCount = 0 #Resetting counter
            #If finished iterating, but last multi-paragraph chunk is below user defined number, add it to token list
            if tempParStr != '':
                #If just extra newline characters, do nothing
                if tempParStr.strip() != '':
                    self.tokenizedList.append(tempParStr.strip())

    #Function normalizes tokens by making them all lowercase
    def normalizeTokens(self):
        for count, token in enumerate(self.tokenizedList):
            self.tokenizedList[count] = token.lower()

    #Function checks parenthesis and makes sure # of '(' match # of ')'
    def checkQueryParenthesis(self, queryString):
        begParenCount = 0
        endParenCount = 0

        for character in queryString:
            #Adds to '(' count
            if character == '(':
                begParenCount += 1
            #Adds to ')' count
            elif character == ')':
                endParenCount += 1
        
        if begParenCount == endParenCount:
            return True 
        else:
            return False 
    
    #Function converts boolean algebra query in infix notation to prefix notation
    #ie: '(not(cat) and not(dog)) or bird' -> ['or', 'and', 'not', 'cat', 'not', 'dog', 'bird']
    def convertToPrefixFromInfix(self, queryString):
        #Priority list, 'not' has a higher priority than 'or' & 'and'
        priorityMap = {'and': 1, 'or': 1, 'not': 2, '(': 0, ')':0}
        operators = ['and', 'or', 'not', '(', ')']
        prefix = []
        stack = []

        #Spliting by both spaces and '('  and ')'
        #Removing empty strings and spaces from list
        splitQuery = list(filter(lambda x: (x != ' ') & (x != ''), re.split('(\W)', queryString)))
        reversedQuery = list(reversed(splitQuery))

        #Infix to Prefix algorithm
        for term in reversedQuery:
            #Operand
            if term not in operators:
                prefix.append(term)
            # ')'
            elif term == ')':
                stack.append(term)
            # '('
            elif term == '(':
                x = stack[-1]
                while x != ')':
                    prefix.append(stack.pop()) 
                    x = stack[-1]
                stack.pop()
            #Operator
            else:
                if len(stack) == 0:
                    stack.append(term)
                else:
                    while True:
                        if len(stack) == 0:
                            stack.append(term)
                            break
                        #Current operator has >= priority than last operator on stack
                        if priorityMap[term] >= priorityMap[stack[-1]]:
                            stack.append(term)
                            break
                        #Current operator has < priority than last operator on stack
                        else:
                            prefix.append(stack.pop())
        #Add any left over operator symbols from stack to prefix list
        while len(stack) > 0:
            prefix.append(stack.pop())

        return list(reversed(prefix))
    
    #Function gets boolean logic query from user for boolean search
    def parseQuery(self):
        while True:
            #User can be shown examples, get help, or enter query
            print("Please enter your boolean logic query\n"
                  "input 'example' to see previous examples\n"
                  "input 'help' for syntax clarification:")

            #So case of operators does not matter
            #All search is based on lowercase inputs
            toParse = input().lower()

            if toParse == 'example':
                print("\n------------------------------------------\n"
                      "Example 1: NOT(cat AND dog) OR bird\n"
                      "Example 2: google AND NOT(apple) AND 95050\n"
                      "------------------------------------------\n")

            elif toParse == 'help':
                print("\n----------------------------------------------------------------------\n"
                      "Allowed operators: NOT, AND, OR \n"
                      "Operators may be capitalized or lowercase\n\n"
                      "Parenthesis and nested parenthesis are allowed\n"
                      "Words are numbers are allowed\n\n"
                      "Words, even proper nouns, with a space must be joined with an operator\n"
                      "Example: San AND Francisco\n"
                      "----------------------------------------------------------------------\n")

            #User has inputed query
            else:
                #Checking parenthesis to make sure same # of '(' as ')'
                result = self.checkQueryParenthesis(toParse)
                if result == False:
                    print('\nQUERY IS NOT VALID, mismatching parenthesis\n')
                else:
                    #Converting query from infix string to prefix list
                    prefixQS = self.convertToPrefixFromInfix(toParse)
                    return prefixQS 

    #Function gets free-form query from user for free-form search
    def inputQuery(self, pastLimit):
        limit = pastLimit

        while True:
            #User can be shown examples, get help, enter query, or modify result limit
            print("Please enter your free-form search query\n"
                  "input 'example' to see previous examples\n"
                  "input 'help' for syntax clarification\n"
                  "input 'limit=<integer>' to limit number of responses\n"
                  "input 'limit=all' to show all responses:")
            
            #All search is based on lowercase inputs
            inputResponse = input().lower()
            
            if inputResponse == 'example':
                print("\n------------------------------------------\n"
                      "Example 1: What is the capital of California?\n"
                      "Example 2: Did the economy grow in 2020\n"
                      "------------------------------------------\n")
            
            elif inputResponse == 'help':
                print("\n----------------------------------------------------------------------\n"
                      "Any free-form text is allowed\n"
                      "Text may be uppercase or lowercase\n"
                      "Numbers, punctuation, and symbols are allowed\n"
                      "You cannot search exclusively by symbol or punctuation\n"
                      "----------------------------------------------------------------------\n")
            #Query or result limit is being modified
            else: 
                limitCheck = inputResponse.split('=')
                #Seeing if result limit is being modified or not, if so, it must be 'all' or a digit
                if (len(limitCheck) > 1) & (limitCheck[0] == 'limit'):
                    #If 'all' is present, no limit is set
                    if limitCheck[1] == 'all':
                        limit = None 
                    #Must be a valid digit, if not, user input is ignored
                    elif limitCheck[1].isdigit() == True:
                        limit = int(limitCheck[1])
                    print('')

                #Query was entered
                else:
                    return inputResponse, limit 
