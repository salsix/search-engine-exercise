"""
This file contains your code to create the inverted index. Besides implementing and using the predefined tokenization function (text2tokens), there are no restrictions in how you organize this file.
predefined functions if available.
"""
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import lxml.html as ET
import invertedindex as idx
import re
import os
import time
import datetime
import pickle
from pymongo import MongoClient

client = MongoClient()
db = client['GIR20']
db_articles = db.articles

def text2tokens(text):
    """
    lowercasing, stopword removal, stemming
    :param text: a text string
    :return: a tokenized string with preprocessing (e.g. stemming, stopword removal, ...) applied

    Problems/TODO:
    - stop word deletion very slow -> use smaller list of words (siehe LVA Forum)
    - Special character stripping & stemming: e.g. heavy-hearted => heavyheart
    - Umlaut-Stripping?
    - http-Link-tokens irrelevant? => e.g. httpwwwdinosauriacomdmlcladosauropodahtml
    """
    porst = PorterStemmer()
    lower = text.casefold()
    tokens = ""
    for word in lower.split():
        # if word in stopwords.words('english'):
        #     continue
        alphaNumOnly = re.sub(r'[^a-zA-Z0-9 ]', '', word)
        token = porst.stem(alphaNumOnly)
        tokens += token + " "

    return tokens[:-1]

def xml2index(artLocation, outFile, index):
    # index = idx.InvertedIndex()
    xmlTree = ET.parse(artLocation)
    articles = xmlTree.xpath('//article')
    artCount = len(articles)
    counter = 1
    startTime = time.time()
    # Collect for faster insertss
    documents = []
    for a in articles:
        # reduce number of articles for quick testing:
        # if (counter > 1):
        #     continue
        artID = a.xpath('header/id/text()')[0]
        contentstring = a.xpath('header/title/text()')[0] + a.xpath('bdy/text()')[0]
        tokenstring = text2tokens(contentstring)
        token = tokenstring.split(" ")

        for tk in token:
            index.add(tk, artID)

        article_data = {'id': int(artID), 'wc': len(token), 'text': contentstring }
        documents.append(article_data)

        perc = round(((counter-1) / artCount) * 100)
        print("     Working on article " + str(counter) + " of " + str(artCount) + "...   (" + str(perc) + "% done)")
        counter += 1

    db_articles.insert_many(documents)
    pickle.dump(index, outFile)

    print("     Done. Execution Time: " + str(datetime.timedelta(seconds=round(time.time() - startTime))))

def set2index(setLocation, outFileName):
    outfile = open(outFileName, 'wb')
    index = idx.InvertedIndex()
    startTime = time.time()
    fileCount = len(os.listdir(setLocation))
    counter = 1
    outfile = open(outFileName, 'wb')
    for file in os.scandir(setLocation):
        perc = round(((counter - 1) / fileCount) * 100)
        print("File " + str(counter) + " of " + str(fileCount) + "...   (" + str(perc) + "% done)")
        xml2index(file.path, outfile, index)
        counter += 1

    pickle.dump(index, outfile)

    print("Done. Execution Time: " + str(datetime.timedelta(seconds=round(time.time() - startTime))))


def frequency(word, index):
     tk = text2tokens(word)
     ix = pickle.load(open(index, 'rb'))
     if word not in ix.index.keys():
         return tk + "not found."
     else:
        for key in ix.index.keys():
             if(word == key):
                 return "found in " + str(ix.index[key])
     return "error"




#set2index('../data/dev-set', 'testtesttest')


# def testsearch(word, index):
#     tk = text2tokens(word)
#     ix = pickle.load(open(index, 'rb'))
#     if word not in ix.index.keys():
#         return tk + "not found."
#     else:
#         for key in ix.index.keys():
#             if(word == key):
#                 return "found in " + str(ix.index[key])
#     return "error"
#
# article2index('dev-set/1.xml', 'testindex')
# print(testsearch('ewfeiwfew', 'testindex'))

# print(pickle.load(open('testindex','rb')))
