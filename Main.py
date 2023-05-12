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
# The total file count is returned.
def buildIndex(folderName):
    index = {}                                  # Create an empty dictionary
    paths = pathlib.Path(folderName)            # Get a list of all files and folders in the folder
    filecount = 0                              # Initialize filecount to 0

    for path in paths.iterdir():                # Loop over all files and folders
        if path.is_file():                      # Check if path is a file or a folder 
            filecount += 1                      # If path is a file, increment filecount
            with open(path, "r", errors ='ignore') as file:  # If path is a file, turn HTML into readable text and call tokenize function
                readable = bs(file, "lxml").get_text()
                tokens = tokenize(readable)

                for token in tokens:           # For each token in the tokens dictionary returned by tokenize
                    current_post = Posting.Posting(path.name, tokens[token]) # Create a posting with the document ID and term frequency
                    if token not in index:     # If token is not in index, add token to index
                        index[token] = [current_post]
                    else:                     # If token is in index, add posting to postings list of token in index
                        index[token].append(current_post)
                writeIndex(path, index)

        # If path is a folder, recursively call buildIndex
        else:
            filecount += buildIndex(path)

    # Return overall filecount
    return filecount

# Writes an inverted index to a json file
def writeIndex(path, index):
    with open ("data/index.json", "r") as file:
        if file.read(1):
            file.seek(0)
            data = json.load(file)
        else:
            data = {}
    with open("data/index.json", "w") as file:
        for token in index:
            if token not in data:
                data[token] = index[token]
            else:
                data[token] += index[token]
        
        json.dump(index, file, indent=4)




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



# Make calls to build inverted index, and dump data into a json file
if __name__ == "__main__":
    # Create an empty json file
    with open("data/index.json", "w") as file:
        json.dump({}, file, indent=4)

    filecount = buildIndex("/Users/jerrychen/Desktop/UCI/Spring23/INF141/Assignment3/DEV")
    print(filecount)
    # Count the number of unique tokens in the index by reading the json file
    with open("data/index.json", "r") as file:
        data = json.load(file)
        print(len(data))
    