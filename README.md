# Search Engine: Search Your Documents through Boolean Logic Queries or Free-Form Text Queries

Search Engine is a local, on-disk search engine for your text documents! Either use this program's custom boolean logic query language, based on a boolean retrieval matrix, implemented though a postings list, or write free-form text queries to find
your data! Also, for free-form search queries, determine the specificity of your search algorithm, and determine how specific you want your search results to be: sentence, paragraph, or multi-paragraph!

## Customize Search and Result Specificity
Search Engine allows the user to load their own custom set of documents. This can be text from web pages, training documents, logs, manuals, books, anything that is a '.txt' file. In addition, when you search, regardless of the search method that you use, an entire document will not simply be returned to you, by modifying the '-result' flag to be either 'sentence', 'paragraph', or 'multi-paragraph', the last of which the user can later enter in an integer to specify the exact number of paragraphs, the user can specify exactly how specific any results returned to them are. If the user is doing a free-form query, they also have the additional option to set the '-specificity' flag to be either 'sentence', 'paragraph', or 'multi-paragraph', the last of which the user can later enter in an integer to specify the exact number of paragraphs. This determines how specific the free-form search is, as it splits the documents up to the level specified and calculates the TF-IDF scores and cosine similarities off of these sub-sections. However, if the user sets the '-result' flag to be higher (it can only be equal or higher) than the '-specificity' flag, they can search for a sub-section but display the larger section that the sub-section is found in. For example, the most relevant sentence and the paragraph it is found in.

## Searching by Boolean Logic Queries
The first method, to allow searching by boolean logic queries, is implemented by using a boolean retrieval matrix, that, for efficiency and scalability, is itself implemented using a postings list, which is essentially a list of linked lists, where each linked list is akin to a branch that represents a document's sub-section, depending on how it was split, and the postings, or nodes sequential to the initial head node, contain the tokenized words found in the sub-section. Postings lists are preferable to a pure boolean retrial matrix due to the sparse nature of the matrix, which consumes large amounts of memory when scaled. Additionally, further optimizations were implemented, such as sorted postings, which allow for quicker retrial and the addition of skip pointers, or even hash based pointers, to skip to a certain alphabetical character in O(1) time.

## Searching by Free-Form Text Queries
The second method, to allow searching by free-form text queries, is implemented by taking TF-IDF, or 'Term Frequency - Inverse Document Frequency', scores for each word in a document's sub-section, depending on how it was split, and thus a TF-IDF matrix is computed. The TF-IDF score for each individual word is defined as: 
<p align="center">
    <img src=imgs/tfIdf.png alt="Term Frequency-Inverse Document Frequency Equation"/>
</p>
From here, when the user inputs a query, its own TF-IDF scores, over the entire query and the different subsections, are calculated and using the equation for cosine similarity, defined as: 
<p align="center">
    <img src=imgs/cosSim.png alt="Cosine Similarity Equation"/>
</p>  
we can now see which document sub-section, now a TF-IDF vector, has a similar angle to our own query, itself a TF-IDF vector. This way, length between the subsection and the query do not matter, just how relevant, or the angle theta, between the two. The user can specify how many results are returned or if they want all the results to be returned, and they can constantly reset or modify this setting, while any changes they make to it are remembered.

## Features
- Switch between different search and query types, go back and forth without recomputing
- Search through boolean logic queries using these operators: *AND*, *OR*, *NOT*
- Search through free-form text queries
- In built caching mechanism for free-form text queries, only recomputes for new queries if it has to
- Never has to recompute for additional boolean logic queries
- Efficient placement of postings, allows for skip pointers and hash based pointers with O(1) access time
- Remembers changes to settings, specifically limiting results displayed for free-form text queries

## Examples
### Example Boolean Logic Queries:
```
computer and science and degree
((not(cat) and not(dog)) or bird) or not(penguin and bat)
not(Apple and not(Google) or Microsoft) and Nvidia
```
### Example Free-Form Text Queries:
```
What is the capital of California?
Error 127 why won't my program compile
```
### Example Usage:
```
python searchEngine.py -f=searchFiles -q=Free-Form -r=paragraph -s=sentence
python searchEngine.py -f=differentFiles -q=Boolean -r=sentence
```
## Actual Usage - Boolean Logic Query  
*searchFolder*, included in this Git repo, has text scraped from UC Berkeley and Stanford University's Wikipedia page.
#### To run:
```
python searchEngine.py -f=searchFiles -q=Boolean -r=sentence
```
#### Program Output and User Input:
```
Please enter your boolean logic query
input 'example' to see previous examples
input 'help' for syntax clarification:
computer and science and nobel
```
#### Program Results:
```
-----------------------------------------------
FOUND 2 TOTAL RESULTS

RESULT 1:
The Turing Award, the "Nobel Prize of computer science", has been awarded to 11 alumni and 
12 past and present full-time faculty, with Dana Scott being an alumnus and a faculty member.
IN FILE:
ucBerkeley.txt

RESULT 2:
Stanford's faculty and former faculty includes 46 Nobel laureates, 5 Fields Medalists, as 
well as 16 winners of the Turing Award, the so-called "Nobel Prize in computer science", 
comprising one third of the awards given in its 44-year history.
IN FILE:
stanford.txt
-----------------------------------------------
```
## Actual Usage - Free-Form Text Query  
*searchFolder*, included in this Git repo, has text scraped from UC Berkeley and Stanford University's Wikipedia page.
#### To run:
```
python searchEngine.py -f=searchFiles -q=Free-Form -r=paragraph -s=sentence
```
#### Program Output and User Input:
```
Please enter your free-form search query
input 'example' to see previous examples
input 'help' for syntax clarification
input 'limit=<integer>' to limit number of responses
input 'limit=all' to show all responses:
limit=2

Please enter your free-form search query
input 'example' to see previous examples
input 'help' for syntax clarification
input 'limit=<integer>' to limit number of responses
input 'limit=all' to show all responses:
diverse students sustainability
```
#### Program Results:
```
-----------------------------------------------
FOUND 2 TOTAL RESULTS

RESULT 1:
17% of students receive Pell Grants, a common measure of low-income students at a college.
FOUND IN:
Full-time undergraduate tuition was $42,690 for 2013–2014. Stanford's admission process is 
need-blind for US citizens and permanent residents; while it is not need-blind for international 
students, 64% are on need-based aid, with an average aid package of $31,411. In 2012–13, the 
university awarded $126 million in need-based financial aid to 3,485 students, with an average 
aid package of $40,460. Eighty percent of students receive some form of financial aid. Stanford 
has a no-loan policy. For undergraduates admitted in 2015, Stanford waives tuition, room, and 
board for most families with incomes below $65,000, and most families with incomes below $125,000 
are not required to pay tuition; those with incomes up to $150,000 may have tuition significantly 
reduced. 17% of students receive Pell Grants, a common measure of low-income students at a college.
IN FILE:
stanford.txt

RESULT 2:
During the 2006–07 school year, there were 94 political student groups on campus including 
MEChXA de UC Berkeley, Berkeley American Civil Liberties Union, Berkeley Students for Life, 
Campus Greens, The Sustainability Team (STEAM), the Berkeley Student Food Collective, Students 
for Sensible Drug Policy, Cal Berkeley Democrats, and the Berkeley College Republicans.
FOUND IN:
UC Berkeley has a reputation for student activism, stemming from the 1960s and the Free Speech 
Movement. Today, Berkeley is known as a lively campus with activism in many forms, from email 
petitions, presentations on Sproul Plaza and volunteering, to the occasional protest. During 
the 2006–07 school year, there were 94 political student groups on campus including MEChXA de 
UC Berkeley, Berkeley American Civil Liberties Union, Berkeley Students for Life, Campus Greens, 
The Sustainability Team (STEAM), the Berkeley Student Food Collective, Students for Sensible 
Drug Policy, Cal Berkeley Democrats, and the Berkeley College Republicans. Berkeley sends the 
most students to the Peace Corps of any university in the nation.
IN FILE:
ucBerkeley.txt
-----------------------------------------------
```
## Planned Future Updates:
- There should be a way to write your results to a file if you want that
- Can searching through the postings lists be more efficient?
- Can we rank the results from the boolean retrieval matrix?
- Can you search by topic?  
    - Incorporating document topic segmentation using ML algorithms
