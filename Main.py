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
            with open(path, "r", errors ='ignore') as file:
                readable = bs(file, "lxml").get_text()
                tokens = tokenize(readable)
            # For each token in the tokens dictionary returned by tokenize
                for token in tokens:
                    current_post = Posting.Posting(path.name, tokens[token]) # Create a posting with the document ID and term frequency
                    # If token is not in index
                    if token not in index:
                        # Add token to index
                        index[token] = [current_post]
                    # If token is in index
                    else:
                        # Add posting to postings list of token in index
                        index[token].append(current_post)
                writeIndex(path, index)

        # If path is a folder, recursively call buildIndex
        else:
            buildIndex(path)


# Write a method that writes an inverted index to multiple
# json files based on the first letter of the token. 
def writeIndex(path, index):
    # Sort the tokens alphabetically
    sorted_index = sorted(index.items(), key=lambda x: x[0])

    # Dump the data into json files based on the first letter of the token
    for i in range(0, 26):
        # read file and check whether the token is in the file
        with open("data/" + chr(ord('a') + i) + ".json", "r") as file:
            # check whether the file is empty
            if file.read(1):
                file.seek(0)
                data = json.load(file)
            else:
                data = {}
        with open("data/" + chr(ord('a') + i) + ".json", "w") as file:
            # if token is not in the file, add the token and its posting to the file
            if sorted_index[i][0] not in data:
                data[sorted_index[i][0]] = sorted_index[i][1]
            # if token is in the file, append the posting to the token's posting list
            else:
                data[sorted_index[i][0]] += (sorted_index[i][1])

            json.dump(data, file, indent=4)
        
        


# Tokenize function that takes a file path as input and returns
# a dictionary of tokens and their term frequencies.
def tokenize(path):
    # Create an empty int default dictionary
    tokens = defaultdict(int)
    # Open file for reading
    try:
        newtokens = re.findall(r'[a-zA-Z0-9]+', path)   # get all tokens
        for newtoken in newtokens:
            tokens[newtoken.lower()] += 1               # treat token as lowercase, increment its count
    except:
        return tokens   # Return tokens

    return tokens       # Return tokens

'''    
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
'''
'''
# A method that builds an inverted index, sort the tokens
# alphabetically, and dump the data into json files based
# on the first letter of the token.
def buildIndexJSON(folderName):
    # Create an empty dictionary
    index = {}
    # Get a list of all files and folders in the folder
    paths = pathlib.Path(folderName)

    # Loop over all files and folders
    for path in paths.iterdir():
        # Check if path is a file or a folder
        if path.is_file():
            # If path is a file, turn HTML into readable text and call tokenize function
            with open(path, "r", errors ='ignore') as file:
                readable = bs(file, "lxml").get_text()
                tokens = tokenize(readable)
            # For each token in the tokens dictionary returned by tokenize
                for token in tokens:
                    current_post = Posting.Posting(path, tokens[token]) # Create a posting
                    # If token is not in index
                    if token not in index:
                        # Add token to index
                        index[token] = [current_post]
                    # If token is in index
                    else:
                        # Add posting to postings list of token in index
                        index[token].append(current_post)
                writeIndex(index)

        # If path is a folder, recursively call buildIndex
        else:
            index = mergeIndex(index, buildIndex(path))

    # Sort the tokens alphabetically
    sorted_index = sorted(index.items(), key=lambda x: x[0])

    # Dump the data into json files based on the first letter of the token
    for i in range(0, 26):
        with open(chr(ord('a') + i) + ".json", "w") as file:
            json.dump(sorted_index[i], file)

    # Return index  
    return index
'''

# Make calls to build inverted index, and dump data into a json file
if __name__ == "__main__":
    # Create empty json files for each letter
    for i in range(0, 26):
        with open("data/" + chr(ord('a') + i) + ".json", "w") as file:
            json.dump({}, file, indent=4)

    buildIndex("/Users/jerrychen/Desktop/UCI/Spring23/INF141/Assignment3/DEV")