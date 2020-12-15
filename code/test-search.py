import createindex as ci
import loadindexfromdisk as lix
import pickle
import time
import datetime

def testsearch(word, ix):
    startTime = time.time()
    tk = ci.text2tokens(word)
    if tk not in ix.index.keys():
        endTime = (datetime.timedelta(seconds=round(time.time() - startTime)))
        return "\"" + tk + "\"" + "not found. Execution Time: " + str(endTime)
    else:
        for key in ix.index.keys():
            if(tk == key):
                endTime = (datetime.timedelta(seconds=round(time.time() - startTime)))
                return "\"" + tk + "\"" + " found in" + str(ix.index[key]) + " Execution Time: " + str(endTime)
    return "error"

ix = lix.load('dev-set_index')

print(testsearch('f13', ix))
print(testsearch('wing', ix))
print(testsearch('considered', ix))
print(testsearch('consider', ix))

