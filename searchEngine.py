#!/usr/bin/python3
import os
import sys
import argparse
from freeform import FreeForm 
from postingsList import PostingsList
from preprocessing import multParCheckValue, Preprocessing 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'searchEngine.py', \
                                     description = "A local, on-disk search engine for your text documents! Either use this \
                                                    program's custom boolean query language, based on a boolean retrieval matrix \
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
                                a boolean retrieval matrix and posting lists, or 'Free-Form' based on \
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

    #Checking to see if provided folder path exists
    try:
        os.chdir(args.folder[0])
    except:
        sys.exit('Folder path provided is not a valid directory path, program terminating')
    searchDocPath = os.getcwd()

    #Checking each file in folder, each must have a '.txt' extension
    for fileName in os.listdir(searchDocPath):
        extensionCheck = fileName.split('.')
        if not ((len(extensionCheck) != 1) and (extensionCheck[1] == 'txt')):
            sys.exit("Files in 'searchDocuments' folder must be text files with .txt extentions, program terminating")

    #If user provided multi-paragraph flag for '-result' or '-specificity', getting user defined length as input
    specificityMultParLength, resultMultParLength = 2, 2
    if args.specificity[0] == 'multi-paragraph':
        specificityMultParLength = multParCheckValue('specificity')
    if args.results[0] == 'multi-paragraph':
        resultMultParLength = multParCheckValue('results')

    specificityDir = {'sentence': 0, 'paragraph': 1, 'multi-paragraph': specificityMultParLength}
    resultDir = {'sentence': 0, 'paragraph': 1, 'multi-paragraph': resultMultParLength}

    #If '-specificity' flag is not set, default is in str format, if flag is set, it's in list format
    specificity = None
    if type(args.specificity) == str:
        specificity = args.specificity
    else:
        specificity = args.specificity[0]

    #'-result' flag cannot be more specific than '-specificity' flag 
    #ie: if you are searching by paragraph, how can you print sentences?
    if resultDir[args.results[0]] < specificityDir[specificity]:
        sys.exit('Search results specificity cannot be broader than search algorithm specificity, program terminating')

    #For each file in folder, reading and tokenizing text according to '-result' flag
    fileTokenTouplesResults = []
    for fileName in os.listdir(searchDocPath):
        fileObj = Preprocessing(resultDir[args.results[0]], fileName)
        fileObj.readFile()
        fileObj.tokenizeText()
        #Appending text and file info as tuple into list
        fileTokenTouplesResults.append((fileObj.tokenizedList, fileObj.fileName))

    equalBool = 0
    fileTokenTouplesSpecificity = []
    #If '-specificity' flag is the same as '-result' flag, reuse computed tuple list from '-result'
    if resultDir[args.results[0]] == specificityDir[specificity]:
        fileTokenTouplesSpecificity = fileTokenTouplesResults
        equalBool = 1
    #If they are different, read and tokenize text according to '-specificity' flag
    else: 
        for fileName in os.listdir(searchDocPath):
            fileObj = Preprocessing(specificityDir[specificity], fileName)
            fileObj.readFile()
            fileObj.tokenizeText()
        
            fileTokenTouplesSpecificity.append((fileObj.tokenizedList, fileObj.fileName))

    quiteBool = 0
    queryType = args.querytype[0]
    alreadyBuiltBoolean = 0
    alreadyBuiltFreeForm = 0
    limit = None 
    #User can input as many sequential queries as they want until they choose to quit
    while quiteBool != 1:
        if queryType == 'Boolean':
            #Initial postings list, which models a boolean retrieval matrix, is computed only once
            #So sequential queries simply have to search off of this
            if alreadyBuiltBoolean == 0:
                pl = PostingsList()
                pl.buildPostingsList(fileTokenTouplesResults)
                alreadyBuiltBoolean = 1
      
            #Parsing user query which is based on custom boolean algebra query language
            pq = Preprocessing()
            parsedQuery = pq.parseQuery()

            #Searching postings list based on query
            results = pl.searchPostingList(parsedQuery)
            #If query is not logical, or there are mismatching parenthesis
            if results[0] == 0:
                print('INVALID QUERY LOGIC, query terminating')
            #If query is logical, printing results, even if 0 results found
            else:
                pl.printResults(results[1])
        
        elif queryType == 'Free-Form':
            #Tf-Idf matrix is computed off of the initial document list
            #Results are cached based on vocabulary from initial document list
            #Tf-Idf matrix may get re-computed depending on the user query
            if alreadyBuiltFreeForm == 0:
                ff = FreeForm()
                ff.buildMatrix(fileTokenTouplesSpecificity)
                alreadyBuiltFreeForm = 1

            #Getting user query, checking to see if user inputed limit on # of results
            #Setting limit on # of results is carried forward until reset by the user
            iq = Preprocessing()
            inputQuery, limit = iq.inputQuery(limit)

            #Searching Tf-Idf matrix using cosine similarities
            results = ff.searchMatrix(inputQuery)
            #Printing results, even if 0 results found
            ff.printResults(results, fileTokenTouplesResults, equalBool, limit)
       
        responseDict = {'Y': 0, 'N': 1}
        while True:
            #Checking to see if user wants to run another query
            repeatResponse = input('Would you like to run another query? (Y/N) ')
            if repeatResponse in responseDict:
                quiteBool = responseDict[repeatResponse]
                break 
        if repeatResponse == 'Y':
            correctResponses = ['Boolean', 'Free-Form']
            #User has option to switch to a different search type
            #If they switch, go back and forth, or stick with their current one, underlying search data structures will not be lost
            while True:
                queryType = input('Would you like to run a boolean or free-from query? (Boolean/Free-Form) ')
                if queryType in correctResponses:
                    print('')
                    break 
