import createindex as ci
import loadindexfromdisk as lix
import pickle
import time
import datetime

def testsearch(word, indexFile):
    startTime = time.time()
    tk = ci.text2tokens(word)
    ix = lix.load(indexFile)
    if tk not in ix.index.keys():
        endTime = (datetime.timedelta(seconds=round(time.time() - startTime)))
        return "\"" + tk + "\"" + "not found. Execution Time: " + str(endTime)
    else:
        for key in ix.index.keys():
            if(tk == key):
                endTime = (datetime.timedelta(seconds=round(time.time() - startTime)))
                return "\"" + tk + "\"" + " found in" + str(ix.index[key]) + " Execution Time: " + str(endTime)
    return "error"

print(testsearch('f13', 'testtesttest'))
print(testsearch('wing', 'singleStreamTest'))
print(testsearch('considered', 'singleStreamTest'))
print(testsearch('consider', 'singleStreamTest'))
