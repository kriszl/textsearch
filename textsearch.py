"""
script that takes 2 inputs from the user
1 - location of a PDF file to be analyzed
2 - location of a .CSV file to be saved for further graphing and such
possible add some pandas code to do some basic analysis
"""

import csv, sys
import pandas as pd
from tika import parser
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class argException(BaseException):
    def __init__(self):
        print("problem with the args")
try:
    userInputFile = sys.argv[1]
    userOutputFile = sys.argv[2]
    userFileInput = sys.argv[3]
except IndexError:
    raise argException

#if len(sys.argv) > 2 or len(sys.arg) < 2:
#    raise argException

rawUserInput = parser.from_file(userInputFile) # a file that was inputted by the user
processedValue = rawUserInput["content"]

# small text processing
tokens = word_tokenize(processedValue) # stripping
punctuations = ["(", ")", ";", ":", "[", "]", ",", "_", "-"]
stopWords = stopwords.words("english") # possible way to make this changable by user?

# creating our array of keywords if these words are not in stopWords (that is english stopwords)
# and if these words are longer than or equal to 3 charachters
keywords = [word.lower() for word in tokens if not word in stopWords and len(word) >= 3]

myCounter = Counter(keywords)

if userFileInput.lower() == "csv":

    # count the number of keywords

    with open(userOutputFile + ".csv", "w", newline="") as csvfile:
        fieldnames = ["word", "occurence"]
        csv.DictWriter(csvfile, fieldnames=fieldnames).writeheader()
        csv.writer(csvfile).writerows(myCounter.most_common())
elif userFileInput.lower() == "pd":
    finalDict = {"word": [i for i in myCounter.keys()], "occurance": [i for i in myCounter.values()]}
    # that might be ambigous or something

    try:
        manyRows = int(input("How many rows? "))
    except:
        print("not valid input")

    a = pd.DataFrame.from_dict(finalDict)
    a.sort_values(by="occurance", inplace=True, ascending=False)
    print(a.head(n=manyRows))
    # test textholder instead of csv file
    #with open(userOutputFile + ".txt", "w") as outFile:
    #    outFile.write(" ".join(keywords))
