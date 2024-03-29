import loadindexfromdisk as lix
import createindex as crix
import math


class TFIDF:

    def __init__(self, index):
        self.index = index
        self.numberOfDocs = len(index.docLengths)

    def calc_idf(self, token):
        documentfrequency = 0
        if token in self.index.index.keys():
            for key, value in self.index.index[token].appearances.items():
                documentfrequency += 1
        zaehler = self.numberOfDocs
        nenner = documentfrequency + 1 # plus one for good measure und to avoid division by 0
        idf = math.log(zaehler/float(nenner))
        return idf

    def search(self, query):
        # docscores = {}
        # tokenstring = crix.text2tokens(query)
        # for token in tokenstring.split(" "):
        #     idf = self.calc_idf(token)
        #     documentfrequency = 0
        #     if token in self.index.index.keys():
        #         for docID, frequency in self.index.index[token].appearances.items():
        #             tokenscore = frequency*idf
        #             if docID in docscores.keys():
        #                 docscores[docID] += tokenscore
        #             else:
        #                 docscores[docID] = tokenscore
        # return sorted(docscores.items(), key=lambda x: x[1], reverse=True)
        docscores = {}
        for docID in self.index.docLengths.keys():
            docscores[docID] = 0
        tokenstring = crix.text2tokens(query)
        for token in tokenstring.split(' '):
            idf = self.calc_idf(token)
            documentfrequency = 0
            for docID in self.index.docLengths.keys():
                if token in self.index.index.keys() and docID in self.index.index[token].appearances.keys():
                    tokenscore = self.index.index[token].appearances[docID] * idf
                else:
                    tokenscore = 0
                docscores[docID] += tokenscore

        return sorted(docscores.items(), key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    '''
    just for testing
    '''
    index = lix.load('dev-set-index')
    termfreqidf = TFIDF(index)
    termfreqidf.search("test")
