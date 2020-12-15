import loadindexfromdisk as lix
from bm25 import BM25
from tfidf import TFIDF
from pymongo import MongoClient

scoring = 'TFIDF'
other = 'BM25'

client = MongoClient()
db = client['GIR20']
db_articles = db.articles

def list_articles(results, counter):
    for i in range(counter, counter+10):
        # TODO: Ausnahmebehandlung wenn out of range
        art = results[counter + i]
        artID = int(art[0])
        fullart = db_articles.find_one({'id': artID})
        title = fullart['text'].split("\n")[0]
        print("("+str(i+1)+") "+ title)
    print("(p) previous 10 | (n) next 10")
    cmd = input('> ')
    if cmd.isdigit() and int(cmd) in [*range(counter,counter+11)]:
        art = results[counter+int(cmd)-1]
        artID = int(art[0])
        fullart = db_articles.find_one({'id': artID})
        print(fullart['text'])
    elif cmd == 'n':
        list_articles(results, counter+10)
    elif cmd == 'p':
        if counter == 0:
            print('Can\'t go back, this is the first page.')
            list_articles(results, counter)
        else:
            list_articles(results, counter-10)
    list_articles(results, counter)


def exploration_mode(index, bm25, tfidf):
    print("## Exploration mode ##\n Please provide a search query:")
    query = input('> ')
    if query in ['q', 'quit']:
        ui_loop(index, bm25, tfidf)
    elif scoring == 'BM25':
        results = bm25.search(query)
        list_articles(results, 0)
    elif scoring == 'TFIDF':
        results = tfidf.search(query)
        list_articles(results, 0)

    ui_loop(index, bm25, tfidf)

def evaluation_mode(index, bm25, tfidf):
    print("## Evaluation mode ##\n Please choose a topic from the list below")
    print(" (1) Topic \n (2) Topic \n (p) previous 10 | (n) next 10")
    input('> ')
    ui_loop(index, bm25, tfidf)

def ui_loop(index, bm25, tfidf):
    global scoring, other
    print("### Main menu ###")
    print("Scoring: [{}]\nChoose a mode \n (X) Exploration mode \n (E) Evaluation mode \n (S) Switch to {} \n (Q) Quit".format(scoring,other)) 
    cmd = input('> ').lower()
    if cmd in ['x', 'exploration']:
        exploration_mode(index, bm25, tfidf)
    elif cmd in ['e', 'Evaluation']:
        evaluation_mode(index, bm25, tfidf)
    elif cmd in ['q', 'quit']:
        print("Exiting!")
        exit()
    elif cmd in ['s', 'switch']:
        scoring, other = other, scoring
        print("Switch to {}".format(scoring))
        ui_loop(index, bm25, tfidf)
    else:
        print("Unknown command...")
        ui_loop(index, bm25, tfidf)


def main():
    print(" ~ Welcome to our search engine! ~ ")
    print('Preparing index...')
    index = lix.load('../data/dev-set_index')
    bm25 = BM25(index)
    tfidf = TFIDF(index)
    print('Index ready, let\'s go!')
    ui_loop(index, bm25, tfidf)

if __name__ == "__main__":
    main()

