#!/usr/bin/python3
import os
import sys
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'searchEngine.py', \
                                     description = "A local, on disk search engine for your text documents! Either use this \
                                                    program's custom boolean query language, based on a boolean retrival matrix \
                                                    implemented though a posting list, or write free-form text queries to find \
                                                    your data! Also, determine how specific you want your search to be: sentence, \
                                                    paragraph, multi-paragraph!")

    parser.add_argument('-f', '--folder', \
                        nargs = 1, \
                        type=str, \
                        required = True, \
                        help = 'Folder where text documents, to be searched through, are stored')
    parser.add_argument('-q', '--query', \
                        nargs = 1, \
                        type = str, \
                        required = True, \
                        choices = ['Free-Form', 'Boolean'], \
                        help = "The type of query search to be performed, either 'Boolean' based on \
                                a boolean retrival matrix and posting lists, or 'Free-Form' based on \
                                cosine similarities")
    parser.add_argument('-s', '--specificity', \
                        nargs = 1, \
                        type = str, \
                        required = False, \
                        choices = ['sentence', 'paragraph', 'multi-paragraph'], \
                        default = 'paragraph', \
                        help = 'Determines the specificity of the search, either: sentence, paragraph, or \
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

    multParLength = ''
    if args.specificity[0] == 'multi-paragraph':
        multParLength = input('Please enter multi-paragraph length: ')
        while (multParLength.isdigit() == False):
            multParLength = input('Please enter a valid integer: ')
    multParLength = int(multParLength)

    if args.query[0] == 'Boolean':
        postingList = booleanSearch.buildPostingList()

        for fileName in os.listdir(searchDocPath):
            processedText = preprocessing.preprocessFile(fileName)
            postingList.addToPostingList(processedText)

        quitBool = 0
        while quitBool != 1:
            quiteBool = postingList.searchPostingList()
