class IndexNode:

    def __init__(self, token, doc):
        self.token = token
        self.appearances = {doc:1}

    def __str__(self):
        ret = " "
        for key,value in self.appearances.items():
            ret += "(" + str(key) + ", " + str(value) + ")"
        return ret


    def add_appearance(self, doc):
        """
        if app.doc is already a key in appearances, increase the value by 1. if not,
        add the apperance to the list.
        """
        if doc in self.appearances:
            self.appearances[doc] += 1
        else:
            self.appearances[doc] = 1
