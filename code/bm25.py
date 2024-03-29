import loadindexfromdisk as lix
import createindex as crix
import math


class BM25:

    def __init__(self, index, k=2, b=0.5):
        self.index = index
        self.numberOfDocs = len(index.docLengths)
        totallength = 0
        for value in index.docLengths.values():
            totallength += value
        self.avgDocLen = totallength/self.numberOfDocs
        self.k = k
        self.b = b

    def calc_idf(self, token):
        documentfrequency = 0
        if token in self.index.index.keys():
            for key, value in self.index.index[token].appearances.items():
                documentfrequency += 1
        zaehler = self.numberOfDocs - documentfrequency + 0.5
        nenner = documentfrequency + 0.5
        idf = math.log(zaehler/nenner)
        return idf

    def calc_score(self, docID, termfrequency):
        tf = termfrequency
        doclen = self.index.docLengths[docID]
        zaehler = tf * (1 + self.k)
        nenner = tf + self.k * (1 - self.b + self.b * (doclen / self.avgDocLen))
        score = zaehler / nenner
        return score

    def search(self, query):
        # docscores = {}
        # tokenstring = crix.text2tokens(query)
        # for token in tokenstring.split(" "):
        #     idf = self.calc_idf(token)
        #     documentfrequency = 0
        #     if token in self.index.index.keys():
        #         for docID, frequency in self.index.index[token].appearances.items():
        #             documentfrequency += 1
        #             tokenscore = self.calc_score(docID, frequency)*idf
        #             if docID in docscores.keys():
        #                 docscores[docID] += tokenscore
        #             else:
        #                 docscores[docID] = tokenscore
        #     for docID in self.index.docLengths.keys():
        #         if docID in docscores.keys:
        #             pass

        docscores = {}
        for docID in self.index.docLengths.keys():
            docscores[docID] = 0
        tokenstring = crix.text2tokens(query)
        for token in tokenstring.split(' '):
            idf = self.calc_idf(token)
            documentfrequency = 0
            for docID in self.index.docLengths.keys():
                if token in self.index.index.keys() and docID in self.index.index[token].appearances.keys():
                    tokenscore = self.calc_score(docID, self.index.index[token].appearances[docID]) * idf
                else:
                    tokenscore = self.calc_score(docID, 0)
                docscores[docID] += tokenscore

        return sorted(docscores.items(), key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    '''
    just for testing
    '''
    index = lix.load('../data/dev-set_index')
    bmfunfundzwanzig = BM25(index)
    print(bmfunfundzwanzig.search("landslide malaysia Find information about landslides that occur in Malaysia."))

