#!/usr/bin/python3
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
    def __init__(self, specificity):
        specificity = None
        fileContents = None
        tokenizedList = None

    def readFile(self, fileName):
        with open(fileName, 'r') as openFile:
            self.fileContents = openFile.read()

    def tokenizeText(self):
        if self.specificity == 'sententence':
            self.tokenizedList = sent_tokenize(self.fileContents)

        elif self.specificity == 'paragraph':
            self.tokenizedList = self.fileContents.split('\n\n')

    def normalizeTokens(self):
        for count, token in enumerate(self.tokenizedList):
            self.tokenizedList[count] = token.lower()
