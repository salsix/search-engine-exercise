import gzip
import pickle

def load(indexFile):
    print("Unzipping...")
    unzip = gzip.open(indexFile, 'rb')
    print("Unpickling...")
    ix = pickle.load(unzip)
    return ix