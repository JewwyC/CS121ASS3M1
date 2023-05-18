#Main.py
import Posting
import pathlib
import re
import json
from bs4 import BeautifulSoup as bs
from collections import defaultdict

CHUNK_SIZE = 100 * 1024 * 1024  # 100MB

# Build the index from the documents in the given folder.
# Return the number of files indexed.
def buildIndex(folderName):
    paths = pathlib.Path(folderName)
    filecount = 0
    chunkcount = 0

    for path in paths.iterdir():
        if path.is_file():
            index = {}
            filecount += 1
            with open(path, "r", errors='ignore') as file:
                while True:
                    lines = file.readlines(CHUNK_SIZE)
                    if not lines:
                        break

                    readable = bs(''.join(lines), "lxml").get_text()
                    tokens = tokenize(readable)

                    for token in tokens:
                        current_post = Posting.Posting(path.name, tokens[token])
                        if token not in index:
                            index[token] = [current_post]
                        else:
                            index[token].append(current_post)

                    writeIndex(chunkcount, index)
                    chunkcount += 1

        else:
            filecount += buildIndex(path)

    return filecount

# Write the index to a file.
def writeIndex(chunkcount, index):
    with open(f"data/index_{chunkcount}.json", "w") as file:
        data = {token: postings for token, postings in index.items()}
        json.dump(data, file, indent=4)

# Tokenize a document path into tokens.
def tokenize(path):
    tokens = defaultdict(int)
    newtokens = re.findall(r'[a-zA-Z0-9]+', path)
    for newtoken in newtokens:
        tokens[newtoken.lower()] += 1
    return tokens

#  Merge the indexes into a single index.
def mergeIndexes():
    paths = pathlib.Path("data")
    index = {}

    for path in paths.glob("index_*.json"):
        with open(path, "r") as file:
            data = json.load(file)

        for token, postings in data.items():
            if token not in index:
                index[token] = postings
            else:
                index[token] += postings

    with open("data/index.json", "w") as file:
        json.dump(index, file, indent=4)

# Main function.
if __name__ == "__main__":
    filecount = buildIndex("/Users/jerrychen/Desktop/UCI/Spring23/INF141/Assignment3/DEV")
    print(filecount)
    # Merge the indexes.
    mergeIndexes()
    # Test the index.
    # Counts unique tokens.
    with open("data/index.json", "r") as file:
        data = json.load(file)
        print(len(data))

    