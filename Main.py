import Posting
import os
import re
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
    files = os.listdir(folderName)
    # Loop over all files and folders
    for file in files:
        # Create full path
        fullPath = os.path.join(folderName, file)
        # If entry is a file
        if os.path.isfile(fullPath):
            # Call tokenize function
            tokens = tokenize(fullPath)
            # For each token
            for token in tokens:
                # If token is not in dictionary
                if token not in index:
                    # Create empty list for token
                    index[token] = []
                # Create posting object
                posting = Posting.Posting(file, tokens[token])
                # Add posting to postings list for token
                index[token].append(posting)
        # If entry is a folder
        elif os.path.isdir(fullPath):
            # Recursively call buildIndex on the folder
            folderIndex = buildIndex(fullPath)
            # Merge with current index
            index = mergeIndex(index, folderIndex)
    # Return index
    return index


# Tokenize function that takes a file path as input and returns
# a dictionary of tokens and their term frequencies.
def tokenize(path):
    # Create an empty int default dictionary
    tokens = defaultdict(int)
    # Open file for reading
    try:
        with open(path, "r"):
            newtokens = re.findall(r'[a-zA-Z0-9]+', file)   # get all tokens
            for newtoken in newtokens:
                tokens[newtoken.lower()] += 1               # treat token as lowercase, increment its count
    except:
        return tokens   # Return tokens
