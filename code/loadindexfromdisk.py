import gzip
import pickle

def load(indexFile):
    indexloc = '../data/' + indexFile
    print("Unzipping...")
    unzip = gzip.open(indexloc, 'rb')
    print("Unpickling...")
    ix = pickle.load(unzip)
    return ix