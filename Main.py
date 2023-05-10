import Posting
import pathlib
import re
import json
from bs4 import BeautifulSoup as bs
from collections import defaultdict


# Write a method that reads through a folder of documents and
# folders, and builds an inverted index. The inverted index is
# a dictionary of term -> postings list. The postings list is
# a list of Posting objects. Each posting object represents
# a document ID and a term frequency for a particular token.
# The inverted index is returned.
def buildIndex(folderName):
    # Create an empty dictionary
    index = {}
    # Get a list of all files and folders in the folder
    paths = pathlib.Path(folderName)

    # Loop over all files and folders
    for path in paths.iterdir():
        # Check if path is a file or a folder
        if path.is_file():
            # If path is a file, turn HTML into readable text and call tokenize function
            with open(path, "r") as file:
                readable = bs(file.read(), "lxml").get_text()
                tokens = tokenize(readable)
            # For each token in the tokens dictionary returned by tokenize
            for token in tokens:
                # If token is not in index
                if token not in index:
                    # Add token to index
                    index[token] = [Posting.Posting(path, tokens[token])]
                # If token is in index
                else:
                    # Add posting to postings list of token in index
                    index[token].append(Posting.Posting(path, tokens[token]))
        # If path is a folder, recursively call buildIndex
        else:
            index = mergeIndex(index, buildIndex(path))

    # Return index  
    return index

# Write a method that merges two inverted indexes. The indexes
# are dictionaries of term -> postings list. The postings list
# is a list of Posting objects. Each posting object represents
# a document ID and a term frequency for a particular token.
def mergeIndex(index1, index2):
    # For each token in index2
    for token in index2:
        # If token is not in index1
        if token not in index1:
            # Add token to index1
            index1[token] = index2[token]
        # If token is in index1
        else:
            # Add postings from index2 to postings list of token in index1
            index1[token] += index2[token]
    # Return merged index
    return index1


# Tokenize function that takes a file path as input and returns
# a dictionary of tokens and their term frequencies.
def tokenize(path):
    # Create an empty int default dictionary
    tokens = defaultdict(int)
    # Open file for reading
    try:
            newtokens = re.findall(r'[a-zA-Z0-9]+', readable)   # get all tokens
            for newtoken in newtokens:
                tokens[newtoken.lower()] += 1               # treat token as lowercase, increment its count
    except:
        return tokens   # Return tokens

    return tokens       # Return tokens


# A method that builds an inverted index, and dump the data into a new json file.
def buildIndexJSON(folderName):
    with open('data/tokenIndex.json', 'w') as file:
        # Call buildIndex to get inverted index
        index = buildIndex(folderName)
        # Write inverted index to a json file
        json.dump(index, file, indent=4)

# Make calls to build inverted index, and dump data into a json file
if __name__ == "__main__":
    buildIndexJSON("/Users/jerrychen/Desktop/UCI/Spring23/INF141/Assignment3/DEV")