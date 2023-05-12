import json

# Write a class that represents a posting in the inverted index.
# A posting is a document ID and a term frequency for a particular
# token in a document. 
class Posting:
    def __init__(self, docID, termFreq):
        self.docID = docID
        self.termFreq = termFreq

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
    

    # Make it JSON serializable
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

# test whether a posting object can be converted to json
p = Posting(1, 2)
print(p.toJSON())

