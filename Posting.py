import json

# Write a class that represents a posting in the inverted index.
# A posting is a document ID and a term frequency for a particular
# token in a document. Inherent from the dict class so that it can
# be converted to JSON.
class Posting(dict):
    def __init__(self, docID, termFreq):
        dict.__init__(self, docID=str(docID), termFreq=termFreq)

    def getDocID(self):
        return self.docID

    def getTermFreq(self):
        return self.termFreq

    def setDocID(self, docID):
        self.docID = docID

    def setTermFreq(self, termFreq):
        self.termFreq = termFreq

    def __str__(self):
        return str(self.docID) + " " + str(self.termFreq)
    


