#!/usr/bin/python3
import os
import sys
import argparse
from preprocessing import multParCheckValue
from postingsList import PostingsList

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'searchEngine.py', \
                                     description = "A local, on-disk search engine for your text documents! Either use this \
                                                    program's custom boolean query language, based on a boolean retrival matrix \
                                                    implemented though a posting list, or write free-form text queries to find \
                                                    your data! Also, determine how specific you want your search algorithm and the \
                                                    results to be: sentence, paragraph, or multi-paragraph!")
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
                        required = True, \
                        choices = ['sentence', 'paragraph', 'multi-paragraph'], \
                        help = 'Determines how specific search algorithms are, either: sentence, paragraph, or \
                                multi-paragraph, where the paragraph length is user defined')
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

    if args.specificity[0] == 'multi-paragraph':
        specificityMultParLength = multParCheckValue('specificity')
    if args.results[0] == 'multi-paragraph':
        resultMultParLength = multParCheckValue('results')

    specificityDir = {'sentence': 0, 'paragraph': 1, 'multi-paragraph': specificityMultParLength}
    resultDir = {'sentence': 0, 'paragraph': 1, 'multi-paragraph': resultMultParLength}

    if resultDir[args.results[0]] < specificityDir[args.specificity[0]]:
        sys.exit('Search results specificity cannot be broader than search algorithm specificity, program terminating')

    fileTokenTouples = []
    for fileName in os.listdir(searchDocPath):
        fileObj = Preprocessing(resultDir[args.results[0]], fileName)
        fileObj.readFile()
        fileObj.tokenizeText()
        
        fileTokenTouples.append((fileObj.tokenizedList, fileObj.fileName))

    if args.query[0] == 'Boolean':
        pl = PostingsList()
        pl = pl.buildPostingsList(fileTokenTouples)

        quiteBool = 0
        while quiteBool != 1:
            queryInput = Preprocessing.parseQuery()

            results = pl.searchPostingList(queryInput)
            PostingsList.printResults(results)

            responseDict = {'Y': 0, 'N': 1}
            while True:
                toParse = input('Would you like to run another query? (Y/N)')
                if toParse in responseDict:
                    quiteBool = responseDict[toParse]
                else:
                    break

    if args.query[0] == 'Free-Form':
