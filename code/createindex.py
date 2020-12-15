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
import gzip
from pymongo import MongoClient
import argparse

GLOB_START_TIME = time.time()

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

def xml2index(artLocation, index):
    xmlTree = ET.parse(artLocation)
    articles = xmlTree.xpath('//article')
    artCount = len(articles)
    startTime = time.time()
    counter = 1
    # Collect for faster insertss
    documents = []
    for a in articles:
        # reduce number of articles for quick testing:
        # if (counter > 1):
        #     continue
        artID = a.xpath('header/id/text()')[0]
        contentstring = ""

        if len(a.xpath('header/title/text()')) > 0:
            contentstring += a.xpath('header/title/text()')[0]
        else:
            print("File " + artLocation + ", Art. " + str(artID) + ": No title found.")

        if len(a.xpath('bdy/text()')) > 0:
            contentstring += a.xpath('bdy/text()')[0]
        else:
            print("File " + artLocation + ", Art. " + str(artID) + ": No bodytext found.")

        tokens = text2tokens(contentstring).split(" ")
        for tk in tokens:
            index.add(tk, artID)

        index.docLengths[artID] = len(tokens)
        article_data = {'id': int(artID), 'wc': len(tokens), 'text': contentstring}
        documents.append(article_data)
        counter += 1

    db_articles.insert_many(documents)

    print("     Done. Execution Time: " + str(datetime.timedelta(seconds=round(time.time() - startTime))) + ", time since start: " + str(datetime.timedelta(seconds=round(time.time() - GLOB_START_TIME))))

def set2index(setLocation, outFileName):
    index = idx.InvertedIndex()
    startTime = time.time()
    fileCount = len(os.listdir(setLocation))
    counter = 1
    for file in os.scandir(setLocation):
        perc = round(((counter - 1) / fileCount) * 100)
        print("File " + str(counter) + " of " + str(fileCount) + "...   (" + str(perc) + "% done)")
        xml2index(file.path, index)
        counter += 1

    print("Pickling and Zipping...")
    with gzip.open('../data/' + outFileName, 'wb') as file:
        pickle.dump(index, file)

    print("Done. Execution Time: " + str(datetime.timedelta(seconds=round(time.time() - startTime))))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create index from input folder')
    parser.add_argument('-f', type=str, help='Input folder', required=True)
    parser.add_argument('index', type=str, help='Index file output path')
    args = parser.parse_args()
    set2index(args.f, args.index)
