import indexnode as nd

class InvertedIndex:
    
    def __init__(self):
        self.index = dict()

    def __str__(self):
        ret = ""
        for token in self.index:
            ret += token + str(self.index[token]) + "\n"
        return ret

    def add(self, token, doc):
        if token in self.index:
            self.index[token].add_appearance(doc)
        else:
            self.index[token] = nd.IndexNode(token, doc)