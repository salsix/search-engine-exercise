import loadindexfromdisk as lix
from bm25 import BM25
from tfidf import TFIDF
from pymongo import MongoClient
import lxml.html as parser
import re
import os
import argparse

scoring = 'TFIDF'
other = 'BM25'

client = MongoClient()
db = client['GIR20']
db_articles = db.articles

parser = argparse.ArgumentParser(description='Interact with our search engine index')
parser.add_argument('index', type=str, help='Index file path')
args = parser.parse_args()

print("Preparing the index...")
index = lix.load(args.index)
bm25 = BM25(index)
tfidf = TFIDF(index)
print("Index ready")


def list_articles(results, counter):
    resultlen = len(results)
    if resultlen == 0:
        print("No results for this query. Try another one.")
        exploration_mode()
    for i in range(counter, counter+10):
        # TODO: Ausnahmebehandlung wenn out of range
        if resultlen < i:
            print("End of result list.")
            break
        art = results[counter + i]
        artID = int(art[0])
        fullart = db_articles.find_one({'id': artID})
        title = fullart['text'].split("\n")[0]
        print("("+str(i+1)+") "+ title)
    print("(p) previous 10 | (n) next 10 | (x) back to exploration | (q) back to main menu")
    cmd = input('> ')
    if cmd.isdigit() and int(cmd) in [*range(counter,counter+11)]:
        art = results[counter+int(cmd)-1]
        artID = int(art[0])
        fullart = db_articles.find_one({'id': artID})
        print(fullart['text'])
        list_articles(results, counter)
    elif cmd == 'n':
        os.system('cls')
        list_articles(results, counter+10)
    elif cmd == 'p':
        os.system('cls')
        if counter == 0:
            print('Can\'t go back, this is the first page.')
            list_articles(results, counter)
        else:
            list_articles(results, counter-10)
    elif cmd == 'q':
        ui_loop()
    elif cmd == 'x':
        os.system('cls')
        exploration_mode()
    os.system('cls')
    list_articles(results, counter)


def exploration_mode():
    print("## Exploration mode ##\n Please provide a search query:")
    query = input('> ')
    if query in ['q', 'quit']:
        ui_loop()
    elif scoring == 'BM25':
        results = bm25.search(query)
        list_articles(results, 0)
    elif scoring == 'TFIDF':
        results = tfidf.search(query)
        list_articles(results, 0)

    ui_loop()

def evaluation_mode(runname):
    print("Generating evaluation file...")
    filename = '../retrieval_results/' + scoring + '-title-description_' + runname + '.txt'
    resultfile = open(filename, 'w')
    xmltree = parser.parse('../data/2010-topics.xml')
    topics = xmltree.xpath('//topic')
    counter = 1
    topiccount = len(topics)
    for t in topics:
        os.system('cls')
        print("Evaluating topic " + str(counter) + " of " + str(topiccount) + '...')
        counter += 1
        topicid = t.xpath('@id')[0]
        title = t.xpath('title/text()')[0]
        description = t.xpath('description/text()')[0]
        query = title + ' ' + description
        if scoring == 'BM25':
            results = bm25.search(query)
        elif scoring == 'TFIDF':
            results = tfidf.search(query)
        for i in range(100):
            # topic-id, Q0, doc-id, rank, score, run-name
            resultfile.write(topicid + ' ' + 'Q0 ' + str(results[i][0]) + ' ' + str(i+1) + ' ' + str(results[i][1]) + ' ' + runname)
            resultfile.write('\n')

    resultfile.close()
    print('Evaluation done. Result saved in ' + filename)
    print("(e) back to evaluation | (q) back to main menu")
    cmd = input('> ')
    if cmd == 'q':
        ui_loop()
    elif cmd == 'e':
        os.system('cls')
        evaluation_mode()
    ui_loop()

def ui_loop():
    global scoring, other
    os.system('cls')
    print("### Main menu ###")
    print("Scoring: [{}]\nChoose a mode \n (X) Exploration mode \n (E) Evaluation mode \n (S) Switch to {} \n (Q) Quit".format(scoring,other)) 
    cmd = input('> ').lower()
    if cmd in ['x', 'exploration']:
        os.system('cls')
        exploration_mode()
    elif cmd in ['e', 'Evaluation']:
        os.system('cls')
        print('Please enter a name for this run.')
        runname = input('> ')
        evaluation_mode(runname)
    elif cmd in ['q', 'quit']:
        print("Exiting!")
        exit()
    elif cmd in ['s', 'switch']:
        scoring, other = other, scoring
        print("Switch to {}".format(scoring))
        ui_loop()
    else:
        print("Unknown command...")
        ui_loop()


def main():
    print(" ~ Welcome to our search engine! ~ ")
    ui_loop()

if __name__ == "__main__":
    main()


