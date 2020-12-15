import pickle

indexFile = 'singleStreamTest'
outfile = open('pickleTXT.txt', 'w')

ix = pickle.load(open(indexFile, 'rb'))

outfile.write(str(ix))