#!/usr/bin/python3
import os
import sys
import argparse
from postingsList import PostingsList
from preprocessing import multParCheckValue, Preprocessing 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'searchEngine.py', \
                                     description = "A local, on-disk search engine for your text documents! Either use this \
                                                    program's custom boolean query language, based on a boolean retrival matrix \
                                                    implemented though a posting list, or write free-form text queries to find \
                                                    your data! Also, for free-form search queries, determine the specificity of \
                                                    your search algorithm, and determine how specific you want your search results \
                                                    to be: sentence, paragraph, or multi-paragraph!")
    parser.add_argument('-f', '--folder', \
                        nargs = 1, \
                        type=str, \
                        required = True, \
                        help = 'Folder where text documents, to be searched through, are stored')
    parser.add_argument('-q', '--querytype', \
                        nargs = 1, \
                        type = str, \
                        required = True, \
                        choices = ['Free-Form', 'Boolean'], \
                        help = "The type of query search to be performed, either 'Boolean' based on \
                                a boolean retrival matrix and posting lists, or 'Free-Form' based on \
                                cosine similarities")
    parser.add_argument('-r', '--results', \
                        nargs = 1, \
                        type = str, \
                        required = True, \
                        choices = ['sentence', 'paragraph', 'multi-paragraph'], \
                        help = 'Determines how specific returned search results are, either: sentence, paragraph, or \
                                multi-paragraph, where the paragraph length is user defined') 
    parser.add_argument('-s', '--specificity', \
                        nargs = 1, \
                        type = str, \
                        required = False, \
                        default = 'sentence', \
                        choices = ['sentence', 'paragraph', 'multi-paragraph'], \
                        help = "Determines how specific free-form search algorithm is, either: sentence, paragraph, or \
                                multi-paragraph, where the paragraph length is user defined; 'sentence' by default")
    args = parser.parse_args()

    try:
        os.chdir(args.folder[0])
    except:
        sys.exit('Folder path provided is not a valid directory path, program terminating')
    searchDocPath = os.getcwd()

    for fileName in os.listdir(searchDocPath):
        extensionCheck = fileName.split('.')
        if not ((len(extensionCheck) != 1) and (extensionCheck[1] == 'txt')):
            sys.exit("Files in 'searchDocuments' folder must be text files with .txt extentions, program terminating")

    specificityMultParLength, resultMultParLength = 2, 2
    if args.specificity[0] == 'multi-paragraph':
        specificityMultParLength = multParCheckValue('specificity')
    if args.results[0] == 'multi-paragraph':
        resultMultParLength = multParCheckValue('results')

    specificityDir = {'sentence': 0, 'paragraph': 1, 'multi-paragraph': specificityMultParLength}
    resultDir = {'sentence': 0, 'paragraph': 1, 'multi-paragraph': resultMultParLength}

    specificity = None
    if type(args.specificity) == str:
        specificity = args.specificity
    else:
        specificity = args.specificity[0]

    if resultDir[args.results[0]] < specificityDir[specificity]:
        sys.exit('Search results specificity cannot be broader than search algorithm specificity, program terminating')

    fileTokenTouplesResults = []
    for fileName in os.listdir(searchDocPath):
        fileObj = Preprocessing(resultDir[args.results[0]], fileName)
        fileObj.readFile()
        fileObj.tokenizeText()
        
        fileTokenTouplesResults.append((fileObj.tokenizedList, fileObj.fileName))

    fileTokenTouplesSpecificity = []
    if resultDir[args.results[0]] == specificityDir[args.specificity]:
        fileTokenTouplesSpecificity = fileTokenTouplesResults
    else: 
        for fileName in os.listdir(searchDocPath):
            fileObj = Preprocessing(specificityDir[args.specificity], fileName)
            fileObj.readFile()
            fileObj.tokenizeText()
        
            fileTokenTouplesSpecificity.append((fileObj.tokenizedList, fileObj.fileName))

    quiteBool = 0
    queryType = args.querytype[0]
    alreadyBuiltBoolean = 0
    alreadyBuiltFreeForm = 0

    while quiteBool != 1:
        if queryType == 'Boolean':
            if alreadyBuiltBoolean == 0:
                pl = PostingsList()
                pl.buildPostingsList(fileTokenTouplesResults)
                alreadyBuiltBoolean = 1
      
            pq = Preprocessing()
            parsedQuery = pq.parseQuery()

            results = pl.searchPostingList(parsedQuery)
            if results[0] == 0:
                print('INVALID QUERY LOGIC, query terminating')
            else:
                pl.printResults(results[1])
        
        elif queryType == 'Free-Form':
            if alreadyBuiltFreeForm == 0:
                ff = FreeForm()
                ff.buildMatrix(fileTokenTouplesSpecificity)
                alreadyBuiltFreeForm = 1

            iq = Preprocessing()
            inputQuery = iq.inputQuery()

            results = ff.searchMatrix(inputQuery)
            ff.printResults(results, fileTokenTouplesResults)
       
        responseDict = {'Y': 0, 'N': 1}
        while True:
            repeatResponse = input('Would you like to run another query? (Y/N) ')
            if repeatResponse in responseDict:
                quiteBool = responseDict[repeatResponse]
                break 
        if repeatResponse == 'Y':
            correctResponses = ['Boolean', 'Free-Form']
            while True:
                queryType = input('Would you like to run a boolean or free-from query? (Boolean/Free-Form) ')
                if queryType in correctResponses:
                    print('')
                    break 
